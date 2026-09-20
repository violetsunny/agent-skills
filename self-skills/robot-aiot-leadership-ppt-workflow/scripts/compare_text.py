#!/usr/bin/env python3
"""PPTX 文字与 expected_text.txt 逐字比对（机械校验，不依赖渲染器）。

用法:
  python3 compare_text.py <文件.pptx> <expected_text.txt>

- expected_text.txt 由 extract_expected_text.py 生成，页标记行（=== ... ===）自动剔除
- 双方均去除全部空白后严格相等比对，不做子串放宽
"""

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


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    actual = pptx_text(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8") as f:
        raw = f.read()
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
