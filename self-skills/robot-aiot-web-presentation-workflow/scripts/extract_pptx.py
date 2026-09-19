#!/usr/bin/env python3
"""PPTX 来源提取入口（phase1 输入节）：既有 PPTX → slides.json + assets/，供母稿分析。

用法:
  python3 extract_pptx.py <文件.pptx> -o outdir/

产物:
  - outdir/extracted-slides.json: 逐页文本块（递归展开 GROUP，含 text frame 与表格）
    + 形状构成计数 + 每页图片清单 + 演讲备注
  - outdir/assets/: ppt/media 全部内嵌图片（md5 前 8 位重命名去重）
  - stdout: 页数、文本块数、图片数汇总
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import zipfile

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
    ap.add_argument("-o", "--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    assets_dir = os.path.join(args.outdir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    seen = {}
    with zipfile.ZipFile(args.pptx) as z:
        for name in z.namelist():
            if name.startswith("ppt/media/"):
                data = z.read(name)
                digest = hashlib.md5(data).hexdigest()[:8]
                ext = os.path.splitext(name)[1] or ".bin"
                out_name = f"{digest}{ext}"
                if digest not in seen:
                    with open(os.path.join(assets_dir, out_name), "wb") as f:
                        f.write(data)
                    seen[digest] = out_name

    prs = Presentation(args.pptx)
    slides = []
    for idx, slide in enumerate(prs.slides, 1):
        texts, counts, images = [], {}, []
        for sp in iter_shapes(slide.shapes):
            key = str(sp.shape_type).split(" ")[0]
            counts[key] = counts.get(key, 0) + 1
            if sp.has_text_frame and sp.text_frame.text.strip():
                texts.append(sp.text_frame.text.strip())
            if getattr(sp, "has_table", False) and sp.has_table:
                for row in sp.table.rows:
                    texts.append(" | ".join(c.text.strip() for c in row.cells))
            if sp.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    digest = hashlib.md5(sp.image.blob).hexdigest()[:8]
                    ext = sp.image.ext or "bin"
                    images.append(f"assets/{digest}.{ext}")
                except Exception:
                    images.append(f"<未落盘图片 shape_id={sp.shape_id}>")
        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
        slides.append(
            {
                "page": idx,
                "texts": texts,
                "shape_counts": counts,
                "images": images,
                "notes": notes,
            }
        )

    out_json = os.path.join(args.outdir, "extracted-slides.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "source": os.path.abspath(args.pptx),
                "slide_size_pt": [prs.slide_width / 12700, prs.slide_height / 12700],
                "slides": slides,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    total_texts = sum(len(s["texts"]) for s in slides)
    print(f"页数={len(slides)} 文本块={total_texts} 图片={len(seen)}")
    print(f"extracted-slides.json -> {out_json}")
    print(f"assets -> {assets_dir}")


if __name__ == "__main__":
    main()
