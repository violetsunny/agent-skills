#!/usr/bin/env python3
"""verbatim 保真比对：剥标签比对两版页面纯文本，可选 href 多重集比对。

口径（references/rebuild-mode.md §2）：
  - 剥标签后空串拼接再归一化空白（两侧统一用空串，不能用空格，否则大量假阳性）。
  - void 标签（meta/link/br/img 等 13 个）不计入配对。
  - --skip-classes 整块跳过 = intentional miss 白名单（默认 lead/subtitle/figcap/footer-note/footer/eyebrow/header-eyebrow，
    均为 diagram-design editorial 壳通用组件名）。
  - --href-multiset：文本 diff 不覆盖链接，另行比对全部 a[href] 多重集并输出差集（补 §2 链接口径）。

用法: python3 fidelity_check.py <old.html> <new.html> [--skip-classes a,b,c] [--href-multiset]
exit 0 = 文本 IDENTICAL（带 --href-multiset 时且 href 多重集相等）；exit 1 = 存在差异。仅 stdlib。
"""

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser

SKIP_TAGS = {"svg", "style", "script", "head", "iframe", "title", "meta", "link"}
VOID = {
    "meta",
    "link",
    "br",
    "img",
    "hr",
    "input",
    "area",
    "base",
    "col",
    "embed",
    "source",
    "track",
    "wbr",
}
DEFAULT_SKIP_CLASSES = "lead,subtitle,figcap,footer-note,footer,eyebrow,header-eyebrow"


class Extract(HTMLParser):
    def __init__(self, skip_classes):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.out = []
        self.skip_classes = skip_classes

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            if tag not in VOID:
                self.skip += 1
            return
        if self.skip:
            return
        cls = dict(attrs).get("class", "") or ""
        if any(c in self.skip_classes for c in cls.split()):
            self.skip += 1
            self._skip_tag = tag

    def handle_endtag(self, tag):
        if self.skip:
            if tag in SKIP_TAGS or getattr(self, "_skip_tag", None) == tag:
                self.skip -= 1
                if self.skip == 0:
                    self._skip_tag = None
            return

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def text(path, skip_classes):
    p = Extract(skip_classes)
    p.feed(open(path, encoding="utf-8").read())
    s = "".join(p.out)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def hrefs(path):
    html = open(path, encoding="utf-8").read()
    return Counter(re.findall(r'<a\b[^>]*href="([^"]+)"', html))


def main():
    ap = argparse.ArgumentParser(
        description="verbatim 保真比对（文本 + 可选 href 多重集）"
    )
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--skip-classes", default=DEFAULT_SKIP_CLASSES)
    ap.add_argument("--href-multiset", action="store_true")
    args = ap.parse_args()
    skip_classes = set(args.skip_classes.split(","))
    diff = False
    a, b = text(args.old, skip_classes), text(args.new, skip_classes)
    if a == b:
        print(f"IDENTICAL  {args.old}  ({len(a)} chars)")
    else:
        import difflib

        diff = True
        aw, bw = a.split(" "), b.split(" ")
        sm = difflib.SequenceMatcher(None, aw, bw)
        print(f"DIFF  {args.old}  old={len(a)} new={len(b)}")
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != "equal":
                print(f"  [{op}] OLD: {' '.join(aw[i1:i2])[:300]!r}")
                print(f"        NEW: {' '.join(bw[j1:j2])[:300]!r}")
    if args.href_multiset:
        ca, cb = hrefs(args.old), hrefs(args.new)
        lost, extra = ca - cb, cb - ca
        if not lost and not extra:
            print(f"HREF IDENTICAL  ({sum(ca.values())} links)")
        else:
            diff = True
            print(f"HREF DIFF  old={sum(ca.values())} new={sum(cb.values())}")
            for h, n in sorted(lost.items()):
                print(f"  [lost x{n}] {h}")
            for h, n in sorted(extra.items()):
                print(f"  [extra x{n}] {h}")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
