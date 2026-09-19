#!/usr/bin/env python3
"""上屏零 emoji 断言（headless 跑「禁用 emoji」节自检）。

用法:
  python3 emoji_audit.py <deck.html 或 pages 目录>...

口径:
  - deck 全部文案禁 emoji: 上屏文字、.notes 话术、caption、alt、按钮文案都算
  - 禁段覆盖 emoji 主块与变体选择符 U+FE0F 等；白名单文字符号 ✓ ✕ ★ ✦ → ▸ · ‣ 不在禁段
  - TreeWalker 扫全部文本节点（排除 script/style），无需逐页深链（.notes 也在禁列）
  - 命中 → 输出残留文本，退出码 1
"""

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

AUDIT_JS = r"""
<pre id="__emoji__" style="display:none"></pre>
<script>
(function () {
  var RE = /[\u{1F000}-\u{1FAFF}\u{FE0F}\u{203C}\u{2049}\u{231A}\u{231B}\u{23E9}-\u{23FA}\u{2611}\u{26A0}\u{2705}\u{274C}\u{274E}\u{27A1}\u{2B50}\u{2B55}]/u;
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  var hits = [];
  while (walker.nextNode()) {
    var n = walker.currentNode;
    var p = n.parentElement;
    if (p && !p.closest('script,style') && RE.test(n.nodeValue)) hits.push(n.nodeValue.trim().slice(0, 60));
  }
  document.getElementById('__emoji__').textContent = JSON.stringify(hits);
})();
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        p = c if os.path.sep in c and os.path.exists(c) else which(c)
        if p and os.path.exists(p):
            return p
    print("FAIL 未找到 Chrome/Chromium", file=sys.stderr)
    sys.exit(2)


def audit(chrome, path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    head, sep, _ = src.rpartition("</body>")
    if not sep:
        print(f"FAIL {path} 无 </body>", file=sys.stderr)
        return None
    fd, tmp = tempfile.mkstemp(
        suffix=".html", dir=os.path.dirname(os.path.abspath(path))
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(head + AUDIT_JS + sep)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--virtual-time-budget=6000",
        "--dump-dom",
        "file://" + tmp,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        os.unlink(tmp)
    m = re.search(r'<pre id="__emoji__"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        print(f"FAIL {path} 审计节点未返回", file=sys.stderr)
        return None
    import json

    return json.loads(htmlmod.unescape(m.group(1)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    chrome = find_chrome()
    targets = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            targets += sorted(
                os.path.join(arg, f) for f in os.listdir(arg) if f.endswith(".html")
            )
        else:
            targets.append(arg)
    bad = 0
    for t in targets:
        hits = audit(chrome, t)
        if hits is None:
            bad += 1
        elif hits:
            bad += 1
            print(f"[FAIL] {t}: emoji 残留 {len(hits)} 处")
            for h in hits[:10]:
                print("   ", h)
        else:
            print(f"[OK] {t}")
    print(f"--- emoji 审计汇总: {len(targets)} 文件, 问题 {bad} ---")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
