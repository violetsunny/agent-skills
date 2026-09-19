#!/usr/bin/env python3
"""四值实测（getBoundingClientRect，比截图精确）：overflowPx / bottomWhitespacePx / titleGapPx / navSafeIntrusionPx。

用法:
  python3 measure_four_values.py <单文件deck.html> --pages 8 [-o report.json] [--budget 6000]
  python3 measure_four_values.py <pages目录> --multi

方法:
  - 每页一次 chrome 进程: 单文件 deck 用 #/N 深链（加载即终态），多页形态逐文件
  - 测量前 document.getAnimations().forEach(a=>a.cancel())（无帧 headless 冻结处置，方法论条 6）
  - scale-to-fit 缩放系数 k 折回 1920x1080 画布 px
  - 隐藏页 rect 全 0 测量无效: 深链逐页加载规避

初判（终判仍按 premium-review-fix.md 人工规则）:
  overflowPx > 0            → FAIL（阻塞）
  titleGapPx < 54           → WARN（封面/仪式页豁免，人工确认）
  navSafeIntrusionPx > 0    → WARN（通栏结构容器豁免 [MEASURE-EXEMPT]，人工判读）
  bottomWhitespacePx 异常大 → 只输出原值（修完反查用）
"""

import argparse
import html as htmlmod
import json
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

MEASURE_JS = r"""
<pre id="__measure__" style="display:none"></pre>
<script>
setTimeout(function () {
  document.getAnimations().forEach(function (a) { try { a.cancel(); } catch (e) {} });
  var results = [];
  document.querySelectorAll('section[data-layout], section.slide, .slide, .canvas, .stage').forEach(function (sec) {
    var sr = sec.getBoundingClientRect();
    if (!sr.width && !sr.height) return;
    var k = sr.height / 1080 || 1;
    var overflow = 0, maxBottom = 0;
    sec.querySelectorAll('*').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      if (el.closest('details:not([open])')) return;
      overflow = Math.max(overflow, r.bottom - sr.bottom, r.right - sr.right);
      maxBottom = Math.max(maxBottom, r.bottom);
    });
    var title = sec.querySelector('h1,h2');
    var next = title && title.nextElementSibling;
    results.push({
      layout: sec.dataset.layout || sec.className || '?',
      overflowPx: Math.round(overflow / k),
      bottomWhitespacePx: Math.round((sr.bottom - maxBottom) / k),
      titleGapPx: next ? Math.round((next.getBoundingClientRect().top - title.getBoundingClientRect().bottom) / k) : null,
      navSafeIntrusionPx: Math.round(Math.max(0, maxBottom - (sr.bottom - 86 * k)) / k)
    });
  });
  document.getElementById('__measure__').textContent = JSON.stringify(results);
}, 800);
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        p = c if os.path.sep in c and os.path.exists(c) else which(c)
        if p and os.path.exists(p):
            return p
    print("FAIL 未找到 Chrome/Chromium", file=sys.stderr)
    sys.exit(2)


def inject(deck_path):
    with open(deck_path, encoding="utf-8") as f:
        src = f.read()
    head, sep, _ = src.rpartition("</body>")
    if not sep:
        print(f"FAIL {deck_path} 无 </body>", file=sys.stderr)
        sys.exit(2)
    fd, tmp = tempfile.mkstemp(
        suffix=".html", dir=os.path.dirname(os.path.abspath(deck_path))
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(head + MEASURE_JS + sep)
    return tmp


def measure(chrome, injected_path, deep_link, budget):
    url = "file://" + injected_path + deep_link
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        f"--virtual-time-budget={budget}",
        "--force-prefers-reduced-motion",
        "--dump-dom",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    m = re.search(r'<pre id="__measure__"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        return None
    return json.loads(htmlmod.unescape(m.group(1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--multi", action="store_true")
    ap.add_argument("-o", "--output", default="")
    ap.add_argument("--budget", type=int, default=6000)
    args = ap.parse_args()

    chrome = find_chrome()
    base = os.path.abspath(args.target)
    report = {}
    fails = warns = 0

    tmps = set()
    try:
        if args.multi:
            files = sorted(
                os.path.join(base, f) for f in os.listdir(base) if f.endswith(".html")
            )
            for path in files:
                tmp = inject(path)
                tmps.add(tmp)
                report[os.path.basename(path)] = measure(chrome, tmp, "", args.budget)
        else:
            if not args.pages:
                print("FAIL 单文件 deck 需要 --pages N", file=sys.stderr)
                sys.exit(2)
            tmp = inject(base)
            tmps.add(tmp)
            for n in range(1, args.pages + 1):
                report[f"page-{n}"] = measure(chrome, tmp, f"#/{n}", args.budget)
    finally:
        for t in tmps:
            try:
                os.unlink(t)
            except OSError:
                pass

    for page, vals in report.items():
        if vals is None:
            print(f"[FAIL] {page}: 测量节点未返回（页面加载失败？）")
            fails += 1
            continue
        for v in vals:
            marks = []
            if v["overflowPx"] > 0:
                marks.append("FAIL overflow")
                fails += 1
            if v["titleGapPx"] is not None and v["titleGapPx"] < 54:
                marks.append("WARN titleGap<54（封面/仪式页豁免）")
                warns += 1
            if v["navSafeIntrusionPx"] > 0:
                marks.append("WARN navSafe 侵入（通栏容器可 [MEASURE-EXEMPT]）")
                warns += 1
            tag = " ".join(marks) if marks else "OK"
            print(
                f"[{tag}] {page} {v['layout']}: "
                f"overflow={v['overflowPx']} bottomWS={v['bottomWhitespacePx']} "
                f"titleGap={v['titleGapPx']} navSafe={v['navSafeIntrusionPx']}"
            )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"报告写出 {args.output}")
    print(f"--- 四值汇总: {len(report)} 页, FAIL={fails}, WARN={warns} ---")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
