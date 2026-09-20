#!/usr/bin/env python3
"""PDF 页数断言（interactive-html-authoring.md 打印样式节：交付前 chrome --print-to-pdf 导出后断言 页数 == slide 数）。

用法:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --disable-gpu --print-to-pdf=/tmp/deck.pdf "file://$PWD/index.html"
  python3 pdf_page_count.py /tmp/deck.pdf --expect 8

规则:
  - 页数解析用标准库正则数 /Type /Page 对象（不引 pypdf）；命中 0 时回退读
    页树 /Count 值（对象流压缩的 PDF 数不到明文 /Type /Page）
  - chrome --print-to-pdf 产物（Skia PDF writer）页对象为明文，主路径可数
  - 页数 == 期望 → PASS 退出码 0；不等 → FAIL 退出码 1（打印样式被作用域规则
    压过的典型症状：多页缩到 1-2 页，@media print 的 !important 一个都不能省）
  - 文件不存在 / 非 %PDF 头 → 退出码 2
"""

import argparse
import re
import sys

PAGE_OBJ_RE = re.compile(rb"/Type\s*/Page(?![sA-Za-z])")
COUNT_FALLBACK_RE = re.compile(rb"/Count\s+(\d+)")


def count_pages(data: bytes):
    n = len(PAGE_OBJ_RE.findall(data))
    if n > 0:
        return n, "type-page"
    counts = [int(m.group(1)) for m in COUNT_FALLBACK_RE.findall(data)]
    if counts:
        return max(counts), "count-fallback"
    return 0, "none"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--expect", type=int, required=True, help="期望页数（slide 数）")
    args = ap.parse_args()

    try:
        with open(args.pdf, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"FAIL 读取失败: {e}", file=sys.stderr)
        sys.exit(2)
    if not data.startswith(b"%PDF"):
        print("FAIL 非 PDF 文件（缺 %PDF 头）", file=sys.stderr)
        sys.exit(2)

    pages, method = count_pages(data)
    if method == "none":
        print("FAIL 未解析到页对象（/Type /Page 与 /Count 均无命中）", file=sys.stderr)
        sys.exit(2)
    if method == "count-fallback":
        print(
            f"提示: /Type /Page 明文对象 0 命中（对象流压缩），回退页树 /Count={pages}"
        )

    if pages == args.expect:
        print(f"PASS 页数 {pages} == slide 数 {args.expect}")
        sys.exit(0)
    print(
        f"FAIL 页数 {pages} != slide 数 {args.expect}（检查 @media print 的 !important 是否被作用域规则压过）"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
