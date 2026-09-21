#!/usr/bin/env python3
"""批次级静态验收：禁色 / 骨架六项 / DOM 上限 / 动效种类 / lightbox /
导航链闭合 / lint_deck_html 全量检查集成。

用法: python3 check_deck_batch.py <pages 目录>
退出码: 有 FAIL → 1
"""

import contextlib
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_deck_html

FORBIDDEN = [
    "#0078D4",
    "#003D6B",
    "#E8F4FD",
    "#B85450",
    "#009624",
    "#0078d4",
    "#003d6b",
    "#e8f4fd",
    "#b85450",
    "#009624",
]


def nav_state(s, which):
    m = re.search(r'<a\b[^>]*id="nav-%s"[^>]*href="([^"]+)"' % which, s)
    if m:
        return m.group(1)
    if re.search(r'<span\b[^>]*id="nav-%s"' % which, s):
        return None
    if which == "next" and '<span class="btn">下一页</span>' in s:
        return None
    return "MISSING"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    pages = sorted(glob.glob(os.path.join(sys.argv[1], "p*.html")))
    if not pages:
        print(f"[FAIL] 目录无 p*.html: {sys.argv[1]}")
        sys.exit(1)
    names = [os.path.basename(p) for p in pages]
    fails = []
    for i, p in enumerate(pages):
        name = names[i]
        s = open(p, encoding="utf-8").read()
        tags = len(re.findall(r"<[a-zA-Z][^>]*>", s))
        checks = {
            "stage-1920x1080": "width:1920px" in s and "height:1080px" in s,
            "footer-bar": 'footer class="bar"' in s or "footer class='bar'" in s,
            "h1": "<h1" in s,
            "fit-script": "innerWidth/1920" in s,
            "reduced-motion": "prefers-reduced-motion" in s,
            "data-enter": s.count("data-enter") > 3,
            "pri-#2563eb": "#2563eb" in s,
            "dom<=500": tags <= 500,
            "lightbox": (".lb{" in s and "figure img" in s and "Escape" in s)
            or "<img" not in s,
        }
        bad_colors = [c for c in FORBIDDEN if c in s]
        if bad_colors:
            fails.append(f"{name}: 禁色 {bad_colors}")
        for k, v in checks.items():
            if not v:
                fails.append(f"{name}: {k} FAIL")
        nxt = nav_state(s, "next")
        prv = nav_state(s, "prev")
        if i < len(names) - 1:
            if nxt != names[i + 1]:
                fails.append(f"{name}: 导航链 next={nxt} 应为 {names[i + 1]}")
        elif nxt is not None:
            fails.append(f"{name}: 末页 next 未禁用（{nxt}）")
        if i > 0 and prv != names[i - 1]:
            fails.append(f"{name}: 导航链 prev={prv} 应为 {names[i - 1]}")
        if i == 0 and prv not in (None, "MISSING"):
            fails.append(f"{name}: 首页 prev 未禁用（{prv}）")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            lfails, lwarns = lint_deck_html.lint(p)
        fails.extend(os.path.basename(f) if f.startswith(p) else f for f in lfails)
        anim_kinds = sum(
            k in s for k in ["anim-pop", "anim-draw", "anim-flow", "count"]
        )
        print(
            f"{name}: DOM={tags} anim_kinds={anim_kinds} lint={len(lfails)}F "
            + " ".join(f"{k}={'OK' if v else 'XX'}" for k, v in checks.items())
        )
    print("---")
    if fails:
        print("FAILS:")
        for f in fails:
            print(" ", f)
        sys.exit(1)
    print(f"ALL PASS: {len(pages)} pages")


if __name__ == "__main__":
    main()
