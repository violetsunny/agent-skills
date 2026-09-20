#!/usr/bin/env python3
"""Mermaid → PNG/SVG 构建期渲染器：headless Chrome + CDP 六步管线（纯标准库，自写 WebSocket 客户端）。

用法:
  python3 render_mermaid.py diagram.mmd -o imgs/diagram.png [--svg]
  python3 render_mermaid.py a.mmd b.mmd --out-dir imgs/     # 批量复用同一 Chrome 实例
  cat diagram.mmd | python3 render_mermaid.py - -o out.png  # stdin
  python3 render_mermaid.py diagram.mmd --dry-run           # 无 Chrome 验证管线组装

契约来源: references/diagram-embed-rendering.md §一（1.1 前置 / 1.2 六步 / 1.3 包装页 /
1.4 缓存）、§三（3.1 嵌入决策表 / 3.2 尺寸清晰度）、§四（4.1 降级阶梯 / 4.2 禁止事项）。
包装页模板: templates/mermaid-wrapper.html（§1.3 逐字提取，本脚本填充三处占位）。

六步管线（§1.2）:
  1 启动 headless Chrome（--remote-debugging-port；env MERMAID_RENDER_DEBUG_PORT 优先，
    端口已有存活实例则复用不杀）；轮询 /json/version 超时 30s
  2 templates/mermaid-wrapper.html 填充后经 CDP Page.setDocumentContent 写入（不落盘）
  3 Emulation.setDeviceMetricsOverride 1280×800 dsf=1
  4 每 80ms Runtime.evaluate 轮询 __mermaidReady + #host 包围盒 >0；默认超时 15s；
    __mermaidError 非空立即失败（语法错不重试）；超时类失败上调 30s 重试一次（§4.1）
  5 targetCssWidth = max(cssWidth, minWidth=860)；captureScale = scale×(target/css) 上限 4；
    重设视口后 Page.captureScreenshot clip + captureBeyondViewport → PNG
  6 可选 --svg: Runtime.evaluate 取 #host svg outerHTML

缓存（§1.4）: 键 = sha256(源码去尾空白 + theme + scale + minWidth + background + mermaid版本)
前 12 位 hex；文件 imgs/.mermaid-cache/mermaid-<hash>.png（--svg 时伴生 .svg 一并算命中）；
命中直接复用跳过渲染；参数任一变化即新 hash 天然失效。

降级与禁止（§四）: 找不到 Chrome / mermaid.min.js → exit 2 并打印降级指引（保留源码块 +
diagram-fallback 标注，禁止静默丢图）；渲染失败逐条报「前 40 字符摘要 + 错误」；批量结束
汇报 N 张 / M 成功 / K 降级；临时 profile 目录退出前删除；自启的 Chrome SIGTERM 杀掉。

exit: 0 = 全部成功（含缓存命中/dry-run）；1 = 存在渲染失败；2 = 用法/环境错误。
"""

import argparse
import base64
import hashlib
import json
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "..", "templates", "mermaid-wrapper.html")

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

BG_RE = re.compile(r"^(?:white|transparent|#[0-9a-fA-F]{3,8})$")
PLACEHOLDERS = [
    "background: <white | transparent | #hex>",
    "<已转义的Mermaid源码>",
    'theme: "<default|forest|dark|neutral|base>"',
    "/* mermaid.min.js 全文内联 */",
]


class MermaidSyntaxError(RuntimeError):
    pass


class RenderTimeout(RuntimeError):
    pass


# ---------------------------------------------------------------- WebSocket


def xor_mask(data: bytes, mask: bytes) -> bytes:
    if not data:
        return data
    reps = (len(data) + 3) // 4
    stream = (mask * reps)[: len(data)]
    return (int.from_bytes(data, "big") ^ int.from_bytes(stream, "big")).to_bytes(
        len(data), "big"
    )


class WSClient:
    """RFC6455 客户端（stdlib only）：客户端帧强制 mask，处理 continuation/ping/pong。"""

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, host, port, path, timeout=90):
        self.sock = socket.create_connection((host, port), timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        self.buf = b""
        while b"\r\n\r\n" not in self.buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise RuntimeError("WS 握手期间连接关闭")
            self.buf += chunk
        head, self.buf = self.buf.split(b"\r\n\r\n", 1)
        if b" 101 " not in head.split(b"\r\n")[0] + b" ":
            raise RuntimeError(
                f"WS 握手失败: {head.splitlines()[0].decode(errors='replace')}"
            )
        expect = base64.b64encode(
            hashlib.sha1((key + self.GUID).encode()).digest()
        ).decode()
        if expect.encode() not in head:
            raise RuntimeError("WS Sec-WebSocket-Accept 校验不通过")
        self._id = 0

    def _recv_exact(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(1 << 16)
            if not chunk:
                raise RuntimeError("WS 连接关闭")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _recv_frame(self):
        opcode, chunks = None, []
        while True:
            b1, b2 = self._recv_exact(2)
            fin, op = b1 & 0x80, b1 & 0x0F
            ln = b2 & 0x7F
            if ln == 126:
                ln = int.from_bytes(self._recv_exact(2), "big")
            elif ln == 127:
                ln = int.from_bytes(self._recv_exact(8), "big")
            mask = self._recv_exact(4) if b2 & 0x80 else None
            payload = self._recv_exact(ln) if ln else b""
            if mask:
                payload = xor_mask(payload, mask)
            if op == 0x9:  # ping → pong
                self._send_frame(0xA, payload)
                continue
            if op == 0xA:  # pong 忽略
                continue
            if op == 0x8:
                raise RuntimeError("WS 被对端关闭")
            if opcode is None:
                opcode = op
            chunks.append(payload)
            if fin:
                return opcode, b"".join(chunks)

    def _send_frame(self, opcode, payload):
        head = bytearray([0x80 | opcode])
        ln = len(payload)
        if ln < 126:
            head.append(0x80 | ln)
        elif ln < 65536:
            head.append(0x80 | 126)
            head += ln.to_bytes(2, "big")
        else:
            head.append(0x80 | 127)
            head += ln.to_bytes(8, "big")
        mask = os.urandom(4)
        self.sock.sendall(bytes(head) + mask + xor_mask(payload, mask))

    def send(self, method, params=None, session=None):
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self._send_frame(0x1, json.dumps(msg).encode())
        return self._id

    def wait(self, msg_id, timeout=60):
        deadline = time.time() + timeout
        while True:
            remain = deadline - time.time()
            if remain <= 0:
                raise RenderTimeout(f"CDP 响应超时 (id={msg_id})")
            self.sock.settimeout(remain)
            opcode, data = self._recv_frame()
            if opcode != 0x1:
                continue
            try:
                obj = json.loads(data)
            except ValueError:
                continue
            if obj.get("id") == msg_id:
                if "error" in obj:
                    raise RuntimeError(f"CDP 错误: {obj['error']}")
                return obj.get("result", {})

    def close(self):
        try:
            self._send_frame(0x8, b"")
        except OSError:
            pass
        try:
            self.sock.close()
        except OSError:
            pass


def cdp(ws, method, params=None, session=None, timeout=60):
    return ws.wait(ws.send(method, params, session), timeout)


# ---------------------------------------------------------------- Chrome


def find_chrome():
    env = os.environ.get("MERMAID_RENDER_CHROME_PATH")
    if env:
        return env if os.path.isfile(env) else None
    for c in CHROME_CANDIDATES:
        if os.path.isfile(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def devtools_version(port):
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/json/version", timeout=2
        ) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def wait_devtools(port, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        v = devtools_version(port)
        if v and v.get("webSocketDebuggerUrl"):
            return v
        time.sleep(0.25)
    raise RenderTimeout(f"/json/version {timeout}s 未就绪 (port={port})")


def launch_chrome(path, port, profile):
    return subprocess.Popen(
        [
            path,
            "--headless=new",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}",
            "--disable-gpu",
            "--hide-scrollbars",
            "--disable-blink-features=AutomationControlled",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ---------------------------------------------------------------- 包装页 / 缓存


def load_template():
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        tpl = f.read()
    if tpl.startswith("<!--"):  # 剥离文件头接线说明注释
        tpl = tpl[tpl.find("-->") + 3 :].lstrip("\n")
    return tpl


def build_wrapper(source, theme, background, js):
    html = load_template()
    esc = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = html.replace(PLACEHOLDERS[0], f"background: {background}")
    html = html.replace(PLACEHOLDERS[1], esc)
    html = html.replace(PLACEHOLDERS[2], f'theme: "{theme}"')
    html = html.replace(PLACEHOLDERS[3], js.replace("</script", "<\\/script"))
    for ph in PLACEHOLDERS:
        if ph in html:
            raise RuntimeError(f"包装页占位未替换: {ph}")
    return html


def mermaid_version(js):
    # 压缩产物里 mermaid 自身版本形如 version:"11.x"；依赖可能用 version="x.y.z"，
    # 冒号形态优先，跳过占位 0.0.0；都找不到退回文件哈希（对缓存键更精确）
    for pat in (
        r"""version\s*:\s*["'](\d+\.\d+\.\d+)["']""",
        r"""version\s*=\s*["'](\d+\.\d+\.\d+)["']""",
    ):
        for m in re.finditer(pat, js):
            if m.group(1) != "0.0.0":
                return m.group(1)
    return "sha-" + hashlib.sha256(js.encode("utf-8", "replace")).hexdigest()[:12]


def cache_key(source, theme, scale, min_width, background, version):
    raw = source.rstrip() + theme + str(scale) + str(min_width) + background + version
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def find_mermaid_js(arg):
    cands = []
    if arg:
        cands.append(arg)
    if os.environ.get("MERMAID_RENDER_JS"):
        cands.append(os.environ["MERMAID_RENDER_JS"])
    cands += [
        "assets/mermaid.min.js",
        "vendor/mermaid.min.js",
        os.path.join(SCRIPT_DIR, "..", "assets", "mermaid.min.js"),
        os.path.expanduser("~/.cache/mermaid.min.js"),
    ]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return None


def embed_decision(png_bytes, svg_text):
    """§3.1 决策表。"""
    if svg_text is not None:
        kb = len(svg_text.encode("utf-8")) / 1024
        if kb < 50:
            return f"SVG {kb:.1f}KB <50KB → 直接内联 <svg>（零请求、无限缩放、可被 CSS 定制）"
        return (
            f"SVG {kb:.1f}KB ≥50KB → 内联后总文件 ≤2MB 仍可内联，优先精简图；"
            f"逼近预算改 assets/ 引用"
        )
    kb = len(png_bytes) / 1024
    if kb < 50:
        return f"PNG {kb:.1f}KB <50KB → base64 data URI 内联（self-contained 小图阈值）"
    return f"PNG {kb:.1f}KB ≥50KB → assets/ 文件引用（防单文件体积失控）"


def png_width(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return int.from_bytes(data[16:20], "big")
    return None


# ---------------------------------------------------------------- 渲染

POLL_EXPR = (
    "(function(){var h=document.getElementById('host');"
    "var r=h?h.getBoundingClientRect():null;"
    "return JSON.stringify({ready:window.__mermaidReady===true,"
    "err:window.__mermaidError||null,"
    "box:r?{x:r.x,y:r.y,w:r.width,h:r.height}:null});})()"
)


def render_one(ws, wrapper_html, scale, min_width, timeout, want_svg):
    """§1.2 步骤 2-6，单图独立 page session。返回 (png, svg|None, target_w, cap_scale)。"""
    target_id = session = None
    try:
        target_id = cdp(ws, "Target.createTarget", {"url": "about:blank"})["targetId"]
        session = cdp(
            ws, "Target.attachToTarget", {"targetId": target_id, "flatten": True}
        )["sessionId"]
        cdp(ws, "Page.enable", {}, session)
        cdp(ws, "Runtime.enable", {}, session)
        frame_id = cdp(ws, "Page.getFrameTree", {}, session)["frameTree"]["frame"]["id"]
        cdp(
            ws,
            "Page.setDocumentContent",
            {"frameId": frame_id, "html": wrapper_html},
            session,
            timeout=120,
        )
        cdp(
            ws,
            "Emulation.setDeviceMetricsOverride",
            {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False},
            session,
        )
        deadline = time.time() + timeout
        box = None
        while True:
            res = cdp(
                ws,
                "Runtime.evaluate",
                {"expression": POLL_EXPR, "returnByValue": True},
                session,
                timeout=15,
            )
            val = res.get("result", {}).get("value")
            st = json.loads(val) if val else {}
            if st.get("err"):
                raise MermaidSyntaxError(st["err"])
            b = st.get("box")
            if st.get("ready") and b and b["w"] > 0 and b["h"] > 0:
                box = b
                break
            if time.time() >= deadline:
                raise RenderTimeout(f"{timeout}s 未就绪（__mermaidReady/包围盒）")
            time.sleep(0.08)

        target_w = max(box["w"], min_width)
        cap_scale = min(scale * (target_w / box["w"]), 4)
        cdp(
            ws,
            "Emulation.setDeviceMetricsOverride",
            {
                "width": math.ceil(box["x"] + box["w"] + 16),
                "height": math.ceil(box["y"] + box["h"] + 16),
                "deviceScaleFactor": 1,
                "mobile": False,
            },
            session,
        )
        shot = cdp(
            ws,
            "Page.captureScreenshot",
            {
                "format": "png",
                "clip": {
                    "x": box["x"],
                    "y": box["y"],
                    "width": box["w"],
                    "height": box["h"],
                    "scale": cap_scale,
                },
                "captureBeyondViewport": True,
            },
            session,
            timeout=60,
        )
        png = base64.b64decode(shot["data"])
        svg = None
        if want_svg:
            res = cdp(
                ws,
                "Runtime.evaluate",
                {
                    "expression": "(document.querySelector('#host svg')||{outerHTML:''}).outerHTML",
                    "returnByValue": True,
                },
                session,
            )
            svg = res.get("result", {}).get("value") or None
        return png, svg, target_w, cap_scale
    finally:
        if target_id:
            try:
                cdp(ws, "Target.closeTarget", {"targetId": target_id}, timeout=10)
            except Exception:
                pass


def ws_from_version(ver):
    url = ver["webSocketDebuggerUrl"]  # ws://127.0.0.1:PORT/devtools/browser/GUID
    m = re.match(r"ws://([^:/]+):(\d+)(/.*)$", url)
    if not m:
        raise RuntimeError(f"无法解析 webSocketDebuggerUrl: {url}")
    return WSClient(m.group(1), int(m.group(2)), m.group(3))


FALLBACK_HINT = """降级指引（§4.1-2，禁止静默丢图）: 最终 HTML 中保留转义后的图表源码——
  <div class="diagram-fallback">
    <p class="diagram-fallback-note">图表渲染失败，以下为图表源码（Mermaid）：</p>
    <pre class="mermaid">&lt;转义后的源码&gt;</pre>
  </div>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "sources", nargs="+", help="mermaid 源码文件（.mmd），'-' 读 stdin（仅单源）"
    )
    ap.add_argument(
        "-o", "--output", help="输出 PNG 路径（仅单源；缺省 mermaid-<hash>.png）"
    )
    ap.add_argument("--out-dir", default=".", help="多源输出目录（默认 .）")
    ap.add_argument("--svg", action="store_true", help="同时输出 SVG（§1.2 步骤6）")
    ap.add_argument(
        "--theme",
        default="default",
        choices=["default", "forest", "dark", "neutral", "base"],
    )
    ap.add_argument(
        "--scale", type=float, default=2, help="截图缩放，默认 2，上限 4（§3.2）"
    )
    ap.add_argument(
        "--min-width", type=int, default=860, help="目标显示宽度下限 CSS px，默认 860"
    )
    ap.add_argument(
        "--background", default="white", help="white | transparent | #hex，默认 white"
    )
    ap.add_argument(
        "--mermaid-js", help="本地 mermaid.min.js 路径（禁 CDN；env MERMAID_RENDER_JS）"
    )
    ap.add_argument(
        "--cache-dir",
        default=os.path.join("imgs", ".mermaid-cache"),
        help="渲染缓存目录（§1.4，默认 imgs/.mermaid-cache）",
    )
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument(
        "--timeout",
        type=float,
        default=15,
        help="渲染就绪超时秒，默认 15；超时自动 30s 重试一次（§4.1）",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="只组装管线并打印计划（无 Chrome 也可跑），不渲染",
    )
    args = ap.parse_args()

    if args.scale <= 0:
        print("FAIL --scale 必须 >0", file=sys.stderr)
        sys.exit(2)
    if args.scale > 4:
        print(f"[WARN] scale-cap --scale={args.scale} 超上限 4，按 4 计（§3.2）")
        args.scale = 4.0
    if not BG_RE.match(args.background):
        print(
            f"FAIL --background 非法: {args.background}（white|transparent|#hex）",
            file=sys.stderr,
        )
        sys.exit(2)
    if args.output and len(args.sources) > 1:
        print("FAIL -o 仅支持单源；多源用 --out-dir", file=sys.stderr)
        sys.exit(2)

    # 读源码
    sources = []
    for s in args.sources:
        if s == "-":
            if len(args.sources) > 1:
                print("FAIL stdin '-' 仅支持单源", file=sys.stderr)
                sys.exit(2)
            sources.append(("<stdin>", sys.stdin.read()))
        elif os.path.isfile(s):
            with open(s, encoding="utf-8") as f:
                sources.append((s, f.read()))
        else:
            print(f"FAIL 源码文件不存在: {s}", file=sys.stderr)
            sys.exit(2)
    if not any(src.strip() for _, src in sources):
        print("FAIL mermaid 源码为空", file=sys.stderr)
        sys.exit(2)

    js_path = find_mermaid_js(args.mermaid_js)
    js = None
    if js_path:
        with open(js_path, encoding="utf-8", errors="replace") as f:
            js = f.read()
    version = mermaid_version(js) if js else "no-js"

    jobs = []
    for name, src in sources:
        key = cache_key(
            src, args.theme, args.scale, args.min_width, args.background, version
        )
        if len(sources) == 1 and args.output:
            out_png = args.output
        else:
            out_png = os.path.join(args.out_dir, f"mermaid-{key}.png")
        out_svg = os.path.splitext(out_png)[0] + ".svg" if args.svg else None
        c_png = os.path.join(args.cache_dir, f"mermaid-{key}.png")
        c_svg = os.path.splitext(c_png)[0] + ".svg"
        hit = (
            not args.no_cache
            and os.path.isfile(c_png)
            and (not args.svg or os.path.isfile(c_svg))
        )
        jobs.append(
            {
                "name": name,
                "src": src,
                "key": key,
                "out_png": out_png,
                "out_svg": out_svg,
                "c_png": c_png,
                "c_svg": c_svg,
                "hit": hit,
            }
        )

    chrome = find_chrome()

    if args.dry_run:
        print(
            f"[OK] dry-run chrome: {chrome or '未探测到（正式渲染将 exit 2 走降级）'}"
        )
        port_env = os.environ.get("MERMAID_RENDER_DEBUG_PORT")
        alive = (
            devtools_version(int(port_env)) if port_env and port_env.isdigit() else None
        )
        print(
            f"[OK] dry-run 端口: env={port_env or '未设'} 存活实例={'有(复用)' if alive else '无'} "
            f"计划={'复用' if alive else f'自启 port={port_env or free_port()}'}"
        )
        print(
            f"[OK] dry-run mermaid.min.js: {js_path or '未找到（正式渲染将 exit 2 走降级）'} 版本={version}"
        )
        print(f"[OK] dry-run 缓存目录: {args.cache_dir}")
        for j in jobs:
            wrapper_n = None
            if js:
                wrapper_n = len(
                    build_wrapper(j["src"], args.theme, args.background, js).encode(
                        "utf-8"
                    )
                )
            print(
                f"[OK] dry-run {j['name']}: key={j['key']} 缓存命中={j['hit']} "
                f"输出={j['out_png']}{'+' + j['out_svg'] if j['out_svg'] else ''} "
                f"包装页={f'{wrapper_n / 1024:.0f}KB' if wrapper_n else '未组装(缺 js)'}"
            )
        print(
            "[OK] dry-run CDP 步骤: createTarget→attachToTarget(flatten)→Page.enable/"
            "getFrameTree→setDocumentContent(包装页,不落盘)→setDeviceMetricsOverride"
            "(1280×800)→80ms 轮询 __mermaidReady→测 #host rect→targetCssWidth=max(css,"
            f"{args.min_width})→captureScale=min({args.scale}×ratio,4)→重设视口→"
            "captureScreenshot(clip,captureBeyondViewport)→closeTarget"
        )
        sys.exit(0)

    pending = [j for j in jobs if not j["hit"]]
    for j in jobs:
        if j["hit"]:
            os.makedirs(os.path.dirname(os.path.abspath(j["out_png"])), exist_ok=True)
            if os.path.abspath(j["c_png"]) != os.path.abspath(j["out_png"]):
                shutil.copyfile(j["c_png"], j["out_png"])
            if j["out_svg"] and os.path.abspath(j["c_svg"]) != os.path.abspath(
                j["out_svg"]
            ):
                shutil.copyfile(j["c_svg"], j["out_svg"])
            print(f"[OK] cache-hit {j['name']}: mermaid-{j['key']}.png 复用，跳过渲染")

    ok_n, fail_n = len(jobs) - len(pending), 0
    if pending:
        if not chrome:
            print(
                "FAIL 未找到 Chrome/Chromium/Edge（设 MERMAID_RENDER_CHROME_PATH 指定）",
                file=sys.stderr,
            )
            print(FALLBACK_HINT, file=sys.stderr)
            sys.exit(2)
        if not js:
            print(
                "FAIL 未找到本地 mermaid.min.js（--mermaid-js / env MERMAID_RENDER_JS / "
                "assets|vendor/mermaid.min.js；禁 CDN 运行时拉取）",
                file=sys.stderr,
            )
            print(FALLBACK_HINT, file=sys.stderr)
            sys.exit(2)
        port_env = os.environ.get("MERMAID_RENDER_DEBUG_PORT")
        port = int(port_env) if port_env and port_env.isdigit() else free_port()
        reused = devtools_version(port) is not None
        proc, profile = None, None
        ws = None
        try:
            if reused:
                print(f"[OK] chrome 复用已开启调试端口的实例 port={port}")
            else:
                profile = tempfile.mkdtemp(prefix="mermaid-render-profile-")
                proc = launch_chrome(chrome, port, profile)
            ver = wait_devtools(port, 30)
            ws = ws_from_version(ver)
            for j in pending:
                wrapper = build_wrapper(j["src"], args.theme, args.background, js)
                summary = j["src"].strip()[:40].replace("\n", " ")
                try:
                    try:
                        png, svg, target_w, cap = render_one(
                            ws,
                            wrapper,
                            args.scale,
                            args.min_width,
                            args.timeout,
                            args.svg,
                        )
                    except RenderTimeout as e:
                        print(
                            f"[WARN] retry-30s {j['name']}: 超时类失败（{e}），上调 30s 重试一次（§4.1）"
                        )
                        png, svg, target_w, cap = render_one(
                            ws, wrapper, args.scale, args.min_width, 30, args.svg
                        )
                except (MermaidSyntaxError, RenderTimeout, RuntimeError) as e:
                    fail_n += 1
                    kind = (
                        "语法错误(不重试)"
                        if isinstance(e, MermaidSyntaxError)
                        else "渲染失败"
                    )
                    print(
                        f"[FAIL] render {j['name']}: {kind} 摘要='{summary}' 错误: {e}"
                    )
                    print(FALLBACK_HINT)
                    continue
                os.makedirs(os.path.dirname(os.path.abspath(j["c_png"])), exist_ok=True)
                with open(j["c_png"], "wb") as f:
                    f.write(png)
                if svg is not None:
                    with open(j["c_svg"], "w", encoding="utf-8") as f:
                        f.write(svg)
                if os.path.abspath(j["c_png"]) != os.path.abspath(j["out_png"]):
                    os.makedirs(
                        os.path.dirname(os.path.abspath(j["out_png"])), exist_ok=True
                    )
                    shutil.copyfile(j["c_png"], j["out_png"])
                if j["out_svg"] and os.path.abspath(j["c_svg"]) != os.path.abspath(
                    j["out_svg"]
                ):
                    shutil.copyfile(j["c_svg"], j["out_svg"])
                pw = png_width(png)
                print(
                    f"[OK] render {j['name']}: {j['out_png']} {len(png) / 1024:.1f}KB "
                    f"{pw}px宽 targetCssWidth={target_w:.0f} captureScale={cap:.2f}"
                )
                if pw is not None and pw < target_w * 2:
                    hint = (
                        f"captureScale 已达上限 4，提高 --scale 无效；可降 --min-width 贴近实际图宽，或接受当前清晰度"
                        if cap >= 4
                        else f"提高 --scale 重渲"
                    )
                    print(
                        f"[WARN] clarity {j['name']}: 位图宽 {pw}px < 显示宽 {target_w:.0f}×2，"
                        f"清晰度不足（§3.2 自检）：{hint}"
                    )
                print(
                    f"[OK] embed-decision {j['name']}: {embed_decision(png, svg if args.svg else None)}"
                )
                ok_n += 1
        finally:
            if ws:
                ws.close()
            if proc:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
            if profile:
                shutil.rmtree(profile, ignore_errors=True)

    print(
        f"--- render_mermaid 汇总: {len(jobs)} 张图, {ok_n} 张渲染成功, {fail_n} 张降级 ---"
    )
    if fail_n:
        print(
            "FAIL 存在降级图：最终 HTML 必须保留源码块 + diagram-fallback 标注，禁止静默丢图"
        )
    sys.exit(1 if fail_n else 0)


if __name__ == "__main__":
    main()
