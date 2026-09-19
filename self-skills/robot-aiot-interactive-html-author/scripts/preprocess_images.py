#!/usr/bin/env python3
"""素材图预处理管线（单文件 deck base64 内联 ≤2MB 体积预算）。

用法:
  python3 preprocess_images.py <图片文件或目录> [--max-bytes 1048576] [--max-dim 1200]
                               [--quality 85] [--circle] [--base64]

规则:
  - >max-bytes（默认 1MB）的图 thumbnail 至 max-dim（默认 1200px）再按 quality（默认 85）存 JPEG
  - --circle: 方形 logo 圆形裁剪（透明 PNG 输出）
  - --base64: 额外输出 <名>.b64 文件（data URI 前缀已含），供单文件内联
  - 产物存 _processed 后缀，不覆盖原图
"""

import argparse
import base64
import io
import os
import sys

from PIL import Image

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


def process(path, args):
    im = Image.open(path)
    stem, ext = os.path.splitext(path)
    out_path = stem + "_processed" + ext

    if args.circle:
        from PIL import ImageDraw

        side = min(im.size)
        im = im.convert("RGBA")
        left = (im.width - side) // 2
        top = (im.height - side) // 2
        im = im.crop((left, top, left + side, top + side))
        mask = Image.new("L", (side * 4, side * 4), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, side * 4, side * 4), fill=255)
        mask = mask.resize((side, side), Image.LANCZOS)
        im.putalpha(mask)
        out_path = stem + "_processed.png"

    size = os.path.getsize(path)
    need_resize = size > args.max_bytes or max(im.size) > args.max_dim
    if args.circle or need_resize:
        if need_resize:
            im.thumbnail((args.max_dim, args.max_dim), Image.LANCZOS)
        if args.circle or im.mode in ("RGBA", "P"):
            out_path = stem + "_processed.png"
            im.save(out_path, optimize=True)
        else:
            out_path = stem + "_processed.jpg"
            im.convert("RGB").save(out_path, quality=args.quality, optimize=True)
        print(
            f"OK   {path} ({size}B, {Image.open(path).size}) -> "
            f"{out_path} ({os.path.getsize(out_path)}B, {im.size})"
        )
    else:
        out_path = path
        print(f"SKIP {path}: {size} bytes 未超限，无需处理")

    if args.base64:
        with open(out_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        mime = "image/png" if out_path.endswith(".png") else "image/jpeg"
        b64_path = out_path + ".b64"
        with open(b64_path, "w") as f:
            f.write(f"data:{mime};base64,{data}")
        print(f"     base64 -> {b64_path} ({len(data)} chars)")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--max-bytes", type=int, default=1_048_576)
    ap.add_argument("--max-dim", type=int, default=1200)
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--circle", action="store_true")
    ap.add_argument("--base64", action="store_true")
    args = ap.parse_args()

    if os.path.isdir(args.target):
        files = sorted(
            os.path.join(args.target, f)
            for f in os.listdir(args.target)
            if os.path.splitext(f)[1].lower() in IMG_EXTS and "_processed" not in f
        )
    else:
        files = [args.target]
    if not files:
        print("FAIL 无待处理图片", file=sys.stderr)
        sys.exit(2)
    for f in files:
        process(f, args)
    print(f"--- 预处理汇总: {len(files)} 张 ---")


if __name__ == "__main__":
    main()
