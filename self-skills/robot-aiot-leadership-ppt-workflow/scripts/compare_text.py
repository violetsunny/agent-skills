#!/usr/bin/env python3
"""PPTX 文字与 expected_text.txt 比对（机械校验，不依赖渲染器）。

用法:
  python3 compare_text.py <文件.pptx> <expected_text.txt> [--mode exact|coverage] [--min-coverage 0.8]

- expected_text.txt 由 extract_expected_text.py 生成，页标记行（=== ... ===）自动剔除
- exact（默认）: 双方去除全部空白后严格相等比对，不做子串放宽。
  适用桥接逐字路线（HTML→PPTX 文字逐字保留）
- coverage: expected 按句拆分（。！？；换行分隔，<4 字短句忽略），逐句检查是否
  出现在 PPTX 文字中，输出覆盖率与缺失句清单；覆盖率 < min-coverage 判 FAIL。
  适用 SVG 重绘路线（页内重组允许改写屏上文字，校验目标=关键信息点不丢）
"""

import argparse
import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def iter_shapes(shapes):
    for sp in shapes:
        if sp.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(sp.shapes)
        else:
            yield sp


def pptx_text(path):
    prs = Presentation(path)
    chunks = []
    for slide in prs.slides:
        for sp in iter_shapes(slide.shapes):
            if sp.has_text_frame:
                chunks.append(sp.text_frame.text)
            if getattr(sp, "has_table", False) and sp.has_table:
                for row in sp.table.rows:
                    for cell in row.cells:
                        chunks.append(cell.text)
    return re.sub(r"\s+", "", "".join(chunks))


def coverage_check(actual, raw, min_coverage):
    body = re.sub(r"^===.*===\s*$", "", raw, flags=re.M)
    sentences = [
        re.sub(r"\s+", "", s)
        for s in re.split(r"[。！？；\n]", body)
        if len(re.sub(r"\s+", "", s)) >= 4
    ]
    if not sentences:
        print("FAIL expected 无有效句子")
        sys.exit(1)
    miss = [s for s in sentences if s not in actual]
    hit = len(sentences) - len(miss)
    ratio = hit / len(sentences)
    print(f"coverage: {hit}/{len(sentences)} = {ratio:.1%}")
    if miss:
        print("缺失句:")
        for m in miss:
            print("  -", m[:60])
    if ratio < min_coverage:
        print(f"FAIL 覆盖率 {ratio:.1%} < {min_coverage:.0%}")
        sys.exit(1)
    print("PASS coverage 检查")


def main():
    ap = argparse.ArgumentParser(description="PPTX 文字与 expected_text.txt 比对")
    ap.add_argument("pptx")
    ap.add_argument("expected")
    ap.add_argument("--mode", choices=["exact", "coverage"], default="exact")
    ap.add_argument("--min-coverage", type=float, default=0.8)
    args = ap.parse_args()

    actual = pptx_text(args.pptx)
    with open(args.expected, encoding="utf-8") as f:
        raw = f.read()
    if args.mode == "coverage":
        coverage_check(actual, raw, args.min_coverage)
        return
    raw = re.sub(r"^===.*===\s*$", "", raw, flags=re.M)
    expected = re.sub(r"\s+", "", raw)
    if actual != expected:
        print("FAIL 文字逐字比对不一致")
        print("expected 字数:", len(expected), "actual 字数:", len(actual))
        n = min(len(expected), len(actual))
        for i in range(n):
            if expected[i] != actual[i]:
                lo = max(0, i - 20)
                print(f"首个差异 @ {i}:")
                print("  expected …", expected[lo : i + 20])
                print("  actual   …", actual[lo : i + 20])
                break
        sys.exit(1)
    print("PASS 文字逐字比对一致")


if __name__ == "__main__":
    main()
