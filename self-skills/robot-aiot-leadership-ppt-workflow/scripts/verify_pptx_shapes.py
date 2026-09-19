#!/usr/bin/env python3
"""可编辑 PPTX 硬规则第 4 条：形状构成验证（递归展开 GROUP，计数断言）。

用法:
  python3 verify_pptx_shapes.py <文件.pptx> [--min-textbox 8] [--max-picture-emu 10000000]

断言:
  1. 每页 TEXT_BOX >= min-textbox（默认 8）
  2. 无宽度 > max-picture-emu（默认 10,000,000 EMU）的超尺寸 PICTURE（整页光栅贴图）
任一不过 → FAIL 退出码 1，不得交付，回生成层修复。
"""

import argparse
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def iter_shapes(shapes):
    for sp in shapes:
        if sp.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(sp.shapes)
        else:
            yield sp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--min-textbox", type=int, default=8)
    ap.add_argument("--max-picture-emu", type=int, default=10_000_000)
    args = ap.parse_args()

    prs = Presentation(args.pptx)
    fails = []
    for idx, slide in enumerate(prs.slides, 1):
        counts = {}
        for sp in iter_shapes(slide.shapes):
            key = str(sp.shape_type).split(" ")[0]
            counts[key] = counts.get(key, 0) + 1
            if sp.shape_type == MSO_SHAPE_TYPE.PICTURE:
                w = sp.width or 0
                if w > args.max_picture_emu:
                    fails.append(
                        f"页{idx}: 超尺寸 PICTURE '{sp.name}' 宽 {w} EMU > {args.max_picture_emu}"
                    )
        tb = counts.get("TEXT_BOX", 0)
        if tb < args.min_textbox:
            fails.append(f"页{idx}: TEXT_BOX {tb} < {args.min_textbox}")
        summary = " ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        print(f"页{idx}: {summary}")

    if fails:
        print("FAIL 形状构成验证不通过:")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print(f"PASS 共 {len(prs.slides._sldIdLst)} 页，形状构成验证通过")


if __name__ == "__main__":
    main()
