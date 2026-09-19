#!/usr/bin/env python3
"""通用 headless 注入断言工具（headless 验证方法论条 1/3/6）。

用法:
  python3 headless_assert.py <deck.html> <assert.js> [--deep-link '#/N/M'] [--no-reduced-motion] [--budget 6000]

约定:
  - assert.js 自由编写交互驱动与断言，最终把结果字符串写入 window.__ASSERT_RESULT__
    （建议格式: 每行 "PASS …" 或 "FAIL …"）
  - 本工具用 rpartition('</body>') 注入临时副本（deck 字符串内含 </body> 字面量，replace 会截断）
  - 默认加 --force-prefers-reduced-motion（交互断言走 REDUCED 同步落 DOM 路径）
  - 注入后统一 document.getAnimations().forEach(a=>a.cancel())（无帧 headless 冻结处置）
  - 结果写隐藏节点，--dump-dom 提取；输出含 FAIL 或无结果 → 退出码 1
  - 截图不要用本工具的临时副本（条 7），截图走 screenshot_matrix.py 原始文件
"""

import argparse
import html as htmlmod
import os
import re
import subprocess
import sys
import tempfile
from shutil import which

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

WRAPPER = r"""
<pre id="__assert_result__" style="display:none"></pre>
<script>
document.getAnimations().forEach(function (a) { try { a.cancel(); } catch (e) {} });
window.__ASSERT_RESULT__ = '';
</script>
<script>
%(ASSERT_JS)s
</script>
<script>
setTimeout(function () {
  document.getElementById('__assert_result__').textContent =
    String(window.__ASSERT_RESULT__ || 'FAIL assert.js 未写入 window.__ASSERT_RESULT__');
}, %(SETTLE_MS)d);
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        p = c if os.path.sep in c and os.path.exists(c) else which(c)
        if p and os.path.exists(p):
            return p
    print("FAIL 未找到 Chrome/Chromium", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("assert_js")
    ap.add_argument("--deep-link", default="")
    ap.add_argument("--no-reduced-motion", action="store_true")
    ap.add_argument("--budget", type=int, default=6000)
    ap.add_argument("--settle-ms", type=int, default=3000)
    args = ap.parse_args()

    with open(args.deck, encoding="utf-8") as f:
        src = f.read()
    with open(args.assert_js, encoding="utf-8") as f:
        js = f.read()

    head, sep, _ = src.rpartition("</body>")
    if not sep:
        print("FAIL deck 无 </body>，无法注入", file=sys.stderr)
        sys.exit(2)
    block = WRAPPER.replace("%(ASSERT_JS)s", js).replace(
        "%(SETTLE_MS)d", str(args.settle_ms)
    )
    fd, tmp = tempfile.mkstemp(
        suffix=".html", dir=os.path.dirname(os.path.abspath(args.deck))
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(head + block + sep)

    chrome = find_chrome()
    url = "file://" + tmp + (args.deep_link or "")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        f"--virtual-time-budget={args.budget}",
    ]
    if not args.no_reduced_motion:
        cmd.append("--force-prefers-reduced-motion")
    cmd += ["--dump-dom", url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    finally:
        os.unlink(tmp)

    m = re.search(r'<pre id="__assert_result__"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        print(
            "FAIL dump-dom 未找到结果节点（页面加载失败或注入被截断）", file=sys.stderr
        )
        print(r.stderr[-500:] if r.stderr else "", file=sys.stderr)
        sys.exit(1)
    result = htmlmod.unescape(m.group(1)).strip()
    print(result)
    sys.exit(1 if ("FAIL" in result or not result) else 0)


if __name__ == "__main__":
    main()
