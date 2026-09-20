#!/usr/bin/env python3
"""甲方模板基底重建：删示例页 / 列版式 / 删全屏遮罩 / 删空占位符。

契约来源: references/phase5-ppt-delivery.md:149-193（甲方模板继承 + 基底重建脚本）。

用法:
  python3 init_from_template.py <甲方模板.pptx>                    # 仅打印版式名清单
  python3 init_from_template.py <甲方模板.pptx> --layout-index 1 \
      [--output base_from_template.pptx]                           # 重建基底

规则（phase5:155-159）:
  1. 删掉模板自带示例页，母版/版式/主题/色板一律不动
  2. 版式里铺满全屏的纯色遮罩（>=99% 画布宽高）删除
  3. 新页上版式带来的空占位符删除
  4. 画布尺寸跟模板走，换算比 = 模板宽 pt / HTML 画布宽 px

依赖 python-pptx（与契约脚本一致，本脚本是生成侧而非解析侧）。
"""

import argparse
import sys


def main():
    ap = argparse.ArgumentParser(description="甲方模板基底重建")
    ap.add_argument("template", help="甲方模板 .pptx 路径")
    ap.add_argument(
        "--layout-index",
        type=int,
        default=None,
        help="版式名清单里选定的内页版式序号；不给则只打印清单",
    )
    ap.add_argument("--output", default="base_from_template.pptx", help="输出基底路径")
    args = ap.parse_args()

    try:
        from pptx import Presentation
    except ImportError:
        print("FAIL 缺少 python-pptx: pip3 install python-pptx", file=sys.stderr)
        return 2

    prs = Presentation(args.template)

    for i, layout in enumerate(prs.slide_layouts):
        print(i, layout.name)

    if args.layout_index is None:
        print("已打印版式清单，选定序号后带 --layout-index 重跑")
        return 0

    if not (0 <= args.layout_index < len(prs.slide_layouts)):
        print(
            f"FAIL --layout-index {args.layout_index} 越界（共 {len(prs.slide_layouts)} 个版式）",
            file=sys.stderr,
        )
        return 2

    sld_id_lst = prs.slides._sldIdLst
    for sld_id in list(sld_id_lst):
        prs.part.drop_rel(sld_id.rId)
        sld_id_lst.remove(sld_id)

    layout = prs.slide_layouts[args.layout_index]
    for sp in list(layout.shapes):
        if (
            sp.width
            and sp.height
            and sp.width >= prs.slide_width * 0.99
            and sp.height >= prs.slide_height * 0.99
        ):
            print("删除全屏遮罩:", sp.shape_id, sp.name)
            sp._element.getparent().remove(sp._element)

    slide = prs.slides.add_slide(layout)
    for ph in list(slide.placeholders):
        ph._element.getparent().remove(ph._element)

    prs.save(args.output)
    print("画布 pt:", prs.slide_width / 12700, "x", prs.slide_height / 12700)
    print(f"PASS 写出 {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
