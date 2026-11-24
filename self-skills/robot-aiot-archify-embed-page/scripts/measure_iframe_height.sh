#!/usr/bin/env bash
# 测 archify 产物内容真实高度，输出 iframe 建议高度。
# 用法: measure_iframe_height.sh <archify-html> <iframe内宽> [最大壳高=24000] [png输出路径]
# 内宽必须用探针在真实页面上下文读 iframe.clientWidth，禁公式推算：body/container padding
# 都会减内宽（本 skill 模板窗口 1200 下内宽 = 1200−64−2 = 1134，不是 1198）。
# 口径: wrapper iframe 读 scrollHeight（= max(内容高, 视口高)），从矮壳高向上扫，取最后
# 一次溢出值作内容估计，越过内容高后在 估计+2 处探针验证（vh 联动跳档则迭代）；
# 再做高窗口（≥12000）wrapper 截图 + 右缘灰条像素扫描验证，有灰条（iframe 纵向滚动条）
# 自动加高重验。不饱和类（reader-area 自动放大，scrollH = 壳高 + 常数）与 tree 100vh
# 拉伸（极矮壳高下 scrollH 恒等于壳高）加高无效 → exit 93 报用户裁决，禁改 height。
# 给定 png 输出路径时保留验证截图作证据（放交付目录 _review/）；否则用 /tmp 临时文件并删除。
# 依赖: 系统 Chrome（CHROME_PATH 可覆盖）、python3 + PIL + numpy
# exit: 0=成功 90=Chrome缺失 91=文件缺失 92=截图/探针失败 93=须人工定高
set -u

src="$1"
width="${2:?用法: measure_iframe_height.sh <archify-html> <iframe内宽> [最大壳高] [png输出路径]}"
maxh="${3:-24000}"
out="${4:-}"

CHROME="${CHROME_PATH:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || { echo "[FATAL] Chrome 不存在，用 CHROME_PATH 覆盖" >&2; exit 90; }
[ -f "$src" ] || { echo "[FATAL] 文件不存在: $src" >&2; exit 91; }

if [ -n "$out" ]; then
  mkdir -p "$(dirname "$out")"
else
  out="/tmp/measure_iframe_$$.png"
fi

CHROME="$CHROME" SRC="$src" WIDTH="$width" MAXH="$maxh" OUT="$out" python3 - <<'EOF'
import os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image

chrome = os.environ["CHROME"]
src = os.path.abspath(os.environ["SRC"])
width = int(os.environ["WIDTH"]); maxh = int(os.environ["MAXH"])
out = os.environ["OUT"]
keep = not out.startswith("/tmp/measure_iframe_")

OFFLINE = [
    "--host-resolver-rules=MAP * ~NOTFOUND",
    "--disable-background-networking", "--disable-component-update",
    "--disable-sync", "--disable-domain-reliability", "--disable-breakpad",
    "--no-first-run", "--no-default-browser-check",
    "--disable-features=Translate,OptimizationHints,MediaRouter,DomainReliability",
]

def probe(shell_h):
    wrapper = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:#fff}}
iframe{{width:{width}px;height:{shell_h}px;border:0;display:block}}
</style></head><body>
<iframe id="f" src="file://{src}"></iframe>
<pre id="res">PENDING</pre>
<script>
function report() {{
  var f = document.getElementById('f');
  var d = f.contentDocument;
  if (!d || !d.documentElement) {{ document.getElementById('res').textContent = 'RESULT::NO_ACCESS'; return; }}
  var de = d.documentElement, b = d.body;
  var sh = Math.max(de.scrollHeight, b ? b.scrollHeight : 0);
  document.getElementById('res').textContent =
    'RESULT::scrollHeight=' + sh + ' clientWidth=' + de.clientWidth;
}}
document.getElementById('f').addEventListener('load', function() {{ setTimeout(report, 1200); }});
setTimeout(report, 4000);
</script></body></html>"""
    with tempfile.TemporaryDirectory() as td:
        wp = os.path.join(td, "probe.html")
        with open(wp, "w", encoding="utf-8") as fh:
            fh.write(wrapper)
        cmd = [chrome, "--headless", "--disable-gpu", "--dump-dom",
               f"--window-size={width + 40},{shell_h}",
               "--allow-file-access-from-files", "--virtual-time-budget=9000",
               *OFFLINE, f"file://{wp}"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    m = re.search(r'<pre id="res">RESULT::([^<]*)</pre>', r.stdout)
    if not m:
        print(f"[FATAL] 探针无输出（shell_h={shell_h}）\n{r.stdout[-400:]}\n{r.stderr[-400:]}", file=sys.stderr)
        sys.exit(92)
    txt = m.group(1)
    if txt == "NO_ACCESS":
        print("[FATAL] 跨源拒绝：--allow-file-access-from-files 未生效", file=sys.stderr)
        sys.exit(92)
    return dict((k, int(v)) for k, v in (p.split("=") for p in txt.split()))

# scrollHeight = max(内容高, 视口高)：sh==壳高 只说明「内容装得下」，不是内容高。
# 从矮壳高向上扫，记录最后一次 sh>壳高 的溢出值作内容估计；首次 sh<=壳高 即越过内容高，
# 再在 估计+2 处探针验证（vh 联动产物内容可能随视口跳档，长高则迭代）。
heights = sorted({h for h in [400, 800, 1600, 3200, 6400, 12800, maxh] if h <= maxh})
est = None; hist = []; over_deltas = []; cw = None
for h in heights:
    v = probe(h); sh = v["scrollHeight"]; cw = v["clientWidth"]
    hist.append((h, sh))
    if sh > h:
        over_deltas.append(sh - h)
        if len(over_deltas) >= 3 and over_deltas[-1] > 4 and max(over_deltas[-3:]) - min(over_deltas[-3:]) <= 4:
            print(f"[FATAL] 疑似 reader-area 自动放大（不饱和）：scrollH = 壳高 + 常数（观测 {hist}），"
                  "加高无效。禁改 height，报用户裁决按现状交付。", file=sys.stderr)
            sys.exit(93)
        est = sh
        continue
    if est is None:
        v2 = probe(h // 2); sh2 = v2["scrollHeight"]
        hist.append((h // 2, sh2))
        if sh2 <= h // 2:
            print(f"[FATAL] 疑似 tree 100vh 视口拉伸：极矮壳高下 scrollH 仍恒等于壳高（观测 {hist}）。"
                  "不适合 iframe 嵌入：改 workflow 重出图，或人工定高。", file=sys.stderr)
            sys.exit(93)
        est = sh2
    break
else:
    print(f"[FATAL] 扫到最大壳高 {maxh} 内容仍持续溢出（观测 {hist}），人工定高。", file=sys.stderr)
    sys.exit(93)

final = est + 2
for _ in range(6):
    v = probe(final); sh = v["scrollHeight"]
    hist.append((final, sh))
    if sh <= final:
        break
    final = sh + 2
else:
    print(f"[FATAL] 验证迭代 6 轮内容仍随视口长高（观测 {hist}），人工定高。", file=sys.stderr)
    sys.exit(93)
sat = final - 2

def shoot(iframe_h):
    # 验证必须复现失败上下文：wrapper 内 iframe 定高 + 高窗口（≥12000）整页截图。
    # 顶层直渲产物或矮窗口都复现不出「高窗口下 iframe 出滚动条」陷阱。
    vh = max(12000, iframe_h + 2000)
    wrapper = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:#fff}}
iframe{{width:{width}px;height:{iframe_h}px;border:0;display:block}}
</style></head><body><iframe src="file://{src}"></iframe></body></html>"""
    with tempfile.TemporaryDirectory() as td:
        wp = os.path.join(td, "verify.html")
        with open(wp, "w", encoding="utf-8") as fh:
            fh.write(wrapper)
        cmd = [chrome, "--headless", "--disable-gpu", f"--screenshot={out}",
               f"--window-size={width + 40},{vh}",
               "--virtual-time-budget=6000", *OFFLINE, f"file://{wp}"]
        for attempt in range(3):
            r = subprocess.run(cmd, capture_output=True)
            if r.returncode == 0 and os.path.exists(out):
                a = np.asarray(Image.open(out).convert("RGB"))
                if a.shape[0] >= vh - 2:
                    return a
            print(f"[WARN] Chrome 截图失败或空白（attempt {attempt+1}），重试", file=sys.stderr)
    print("[FATAL] Chrome 截图连续失败", file=sys.stderr)
    sys.exit(92)

def graybar(a):
    band = a[:, max(0, width - 40):width].astype(np.int16)
    r, g, b = band[:, :, 0], band[:, :, 1], band[:, :, 2]
    gray = (np.abs(r - g) < 6) & (np.abs(g - b) < 6) & (r > 150) & (r < 215)
    return float(gray.any(axis=1).mean()) > 0.25

def composited(a):
    region = a[:min(a.shape[0], 12000), :width]
    return int((region < 250).any(axis=2).sum()) > 500

final = sat + 2
a = shoot(final)
status = "none"
if not composited(a):
    a = shoot(final)
if not composited(a):
    status = "unknown（headless 合成盲区，灰条验证失效，须人工整页复核）"
    print("[WARN] iframe 区域空白，灰条验证不可信，须人工整页复核", file=sys.stderr)
elif graybar(a):
    for _ in range(10):
        final += 20
        a = shoot(final)
        if not graybar(a):
            status = f"fixed@{final}"
            break
    else:
        print(f"[FATAL] 加高 10 档仍有右缘灰条（final={final}），人工定高。", file=sys.stderr)
        sys.exit(93)

print(f"inner_width={width} artifact_clientWidth={cw} content_height={sat} "
      f"suggested_height={final} method=saturation graybar={status} probes={len(hist)}")
if not keep:
    os.remove(out)
EOF
rc=$?
exit $rc