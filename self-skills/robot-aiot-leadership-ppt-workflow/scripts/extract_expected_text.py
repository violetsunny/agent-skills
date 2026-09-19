#!/usr/bin/env python3
"""确定性抽取逐页 HTML 的上屏文字，生成 expected_text.txt（零 LLM 参与）。

用法:
  python3 extract_expected_text.py <pages目录|单文件deck.html> [-o expected_text.txt]

- pages 目录模式: 按文件名排序遍历 *.html，每页独立加载抽取
- 单文件 deck 模式: 先探测 .slide 页数，再按 #/N 深链逐页抽取
- 抽取口径: TreeWalker 按文档序收集文本，跳过 .notes 话术容器与 display:none/visibility:hidden 内容
- 注入用 rpartition('</body>')（deck 字符串内含 </body> 字面量，replace 会截断脚本）
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

EXTRACT_JS = r"""
<script>
(function () {
  var out = [];
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  function hidden(el) {
    while (el && el !== document.body) {
      var cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return true;
      el = el.parentElement;
    }
    return false;
  }
  while (walker.nextNode()) {
    var n = walker.currentNode;
    var p = n.parentElement;
    if (!p) continue;
    if (p.closest('script,style,.notes')) continue;
    if (hidden(p)) continue;
    var t = n.nodeValue.replace(/\s+/g, ' ').trim();
    if (t) out.push(t);
  }
  var pre = document.createElement('pre');
  pre.id = '__expected_text__';
  pre.style.display = 'none';
  pre.textContent = out.join('\n');
  document.body.appendChild(pre);
})();
</script>
"""

PROBE_JS = r"""
<script>
(function () {
  var pre = document.createElement('pre');
  pre.id = '__slide_count__';
  pre.style.display = 'none';
  pre.textContent = String(document.querySelectorAll('.slide').length);
  document.body.appendChild(pre);
})();
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.sep in c:
            if os.path.exists(c):
                return c
        else:
            from shutil import which

            p = which(c)
            if p:
                return p
    print(
        "FAIL 未找到 Chrome/Chromium，请安装或改走 sub agent 同口径抽取",
        file=sys.stderr,
    )
    sys.exit(2)


def inject(src_path, js):
    with open(src_path, encoding="utf-8") as f:
        src = f.read()
    head, sep, _ = src.rpartition("</body>")
    if not sep:
        print(f"FAIL {src_path} 无 </body>，无法注入", file=sys.stderr)
        sys.exit(2)
    fd, tmp = tempfile.mkstemp(
        suffix=".html", dir=os.path.dirname(os.path.abspath(src_path))
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(head + js + sep)
    return tmp


def dump_dom(chrome, url, tmp=None):
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        "--virtual-time-budget=6000",
        "--force-prefers-reduced-motion",
        "--dump-dom",
        url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    return r.stdout


def grab(dom, marker_id):
    m = re.search(r'<pre id="%s"[^>]*>(.*?)</pre>' % marker_id, dom, re.S)
    if not m:
        return None
    import html as htmlmod

    return htmlmod.unescape(m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("-o", "--output", default="expected_text.txt")
    args = ap.parse_args()

    chrome = find_chrome()
    pages = []
    if os.path.isdir(args.target):
        pages = sorted(
            os.path.join(args.target, f)
            for f in os.listdir(args.target)
            if f.endswith(".html")
        )
        if not pages:
            print(f"FAIL {args.target} 下无 .html", file=sys.stderr)
            sys.exit(2)
    else:
        pages = [args.target]

    blocks = []
    failures = 0
    for i, page in enumerate(pages, 1):
        if len(pages) == 1 and page.endswith(".html") and os.path.isfile(page):
            probe_tmp = inject(page, PROBE_JS)
            dom = dump_dom(chrome, "file://" + probe_tmp, probe_tmp)
            count = grab(dom, "__slide_count__")
            n = int(count) if count and count.isdigit() else 0
            if n > 1:
                tmp = inject(page, EXTRACT_JS)
                try:
                    for s in range(1, n + 1):
                        dom = dump_dom(chrome, f"file://{tmp}#/{s}")
                        text = grab(dom, "__expected_text__")
                        if text is None:
                            print(
                                f"FAIL 单文件 deck 第 {s}/{n} 页抽取失败",
                                file=sys.stderr,
                            )
                            failures += 1
                            continue
                        blocks.append(f"=== page {s} ===\n{text}")
                finally:
                    try:
                        os.unlink(tmp)
                    except OSError:
                        pass
                continue
        tmp = inject(page, EXTRACT_JS)
        dom = dump_dom(chrome, "file://" + tmp, tmp)
        text = grab(dom, "__expected_text__")
        if text is None:
            print(f"FAIL {page} 抽取失败（dump-dom 无标记节点）", file=sys.stderr)
            failures += 1
            continue
        blocks.append(f"=== page {i} ({os.path.basename(page)}) ===\n{text}")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks) + "\n")
    print(f"写出 {args.output}: {len(blocks)} 页")
    if failures:
        print(f"FAIL {failures} 页抽取失败", file=sys.stderr)
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
