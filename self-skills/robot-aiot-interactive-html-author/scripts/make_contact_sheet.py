#!/usr/bin/env python3
"""构建期并排表（contact sheet）生成器：审查工具，不进交付物。

用法:
  python3 make_contact_sheet.py shots/ -o sheet.html         # HTML 并排表（恒可出，零依赖）
  python3 make_contact_sheet.py shot-*.png -o sheet.png      # PNG 合成（需 Pillow；缺失降级 HTML 并说明）
  python3 make_contact_sheet.py shots/ -o sheet.png --cols 8 --label

契约来源: camera-storyboard.md §14 thumbnail pass「构建期并排表」——
  .contact-sheet: flex wrap / gap 8px / padding 16px / 背景 #808080；
  .thumb: 160×90 overflow hidden。PNG 合成沿用同一几何：缩略图 160×90（cover 裁切）、
  gap 8、padding 16、背景 #808080。批量截图先走 headless 浏览器（screenshot_matrix.py /
  interactive-html-authoring.md headless 验证），本脚本只做并排合成与存档。

目检三件事（§14）:
  1 能量节奏：烈/缓/静分布与四段位一致，无烈页连片、无整排全缓
  2 视觉重复：盖住文字标签后相邻页构图差异仍可辨（否则版式没轮换）
  3 单帧纪律：每张缩略图过 §10 律六（活跃元素 ≤3）与律十（160×90 下最大的词可辨）

口径:
  - 输入 = 截图文件或目录（目录收 .png/.jpg/.jpeg/.webp/.gif），文件名自然排序（p2 < p10）
  - HTML 模式图片 base64 内联（单文件可移动存档）；PNG 模式需 Pillow，ImportError 时
    自动降级写同名 .html 并说明，不中断
  - exit: 0 = 产出成功（含降级）；2 = 用法错误（无图片输入 / 输出后缀不支持 / 不可写）
"""

import argparse
import base64
import math
import os
import re
import sys

THUMB_W, THUMB_H, GAP, PAD = 160, 90, 8, 16
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def nat_key(path):
    name = os.path.basename(path)
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def collect(targets):
    files = []
    for t in targets:
        if os.path.isdir(t):
            files += [
                os.path.join(t, f)
                for f in os.listdir(t)
                if f.lower().endswith(IMG_EXTS)
            ]
        elif os.path.isfile(t):
            files.append(t)
        else:
            print(f"FAIL 输入不存在: {t}", file=sys.stderr)
            sys.exit(2)
    return sorted(files, key=nat_key)


def build_html(paths, label):
    thumbs = []
    for p in paths:
        ext = os.path.splitext(p)[1].lower()
        with open(p, "rb") as f:
            uri = (
                f"data:{MIME.get(ext, 'image/png')};base64,"
                + base64.b64encode(f.read()).decode()
            )
        name = os.path.basename(p)
        cap = f'<div class="label">{name[:40]}</div>' if label else ""
        thumbs.append(f'  <div class="thumb"><img src="{uri}" alt="{name}">{cap}</div>')
    return (
        '<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        "<title>contact sheet（审查工具，不进交付物）</title>\n<style>\n"
        "  body { margin: 0; }\n"
        "  .contact-sheet { display: flex; flex-wrap: wrap; gap: 8px; padding: 16px; background: #808080; }\n"
        "  .contact-sheet .thumb { width: 160px; height: 90px; overflow: hidden; position: relative; }\n"
        "  .contact-sheet .thumb img { width: 160px; height: 90px; object-fit: cover; display: block; }\n"
        "  .contact-sheet .thumb .label { position: absolute; left: 0; right: 0; bottom: 0;\n"
        "    font: 10px/1.4 ui-monospace, monospace; color: #fff; background: rgba(0,0,0,.55);\n"
        "    padding: 1px 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n"
        '</style>\n</head>\n<body>\n<div class="contact-sheet">\n'
        + "\n".join(thumbs)
        + "\n</div>\n</body>\n</html>\n"
    )


def build_png(paths, out, cols, label):
    """Pillow 合成；ImportError 返回 False 由调用方降级。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    n = len(paths)
    rows = math.ceil(n / cols)
    W = PAD * 2 + cols * THUMB_W + (cols - 1) * GAP
    H = PAD * 2 + rows * THUMB_H + (rows - 1) * GAP
    sheet = Image.new("RGB", (W, H), (128, 128, 128))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=11)
    except TypeError:
        font = ImageFont.load_default()
    tr = THUMB_W / THUMB_H
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        ir = im.width / im.height
        if ir > tr:  # cover 裁切到 16:9
            w = int(im.height * tr)
            x = (im.width - w) // 2
            im = im.crop((x, 0, x + w, im.height))
        else:
            h = int(im.width / tr)
            y = (im.height - h) // 2
            im = im.crop((0, y, im.width, y + h))
        im = im.resize((THUMB_W, THUMB_H), Image.LANCZOS)
        r, c = divmod(i, cols)
        x, y = PAD + c * (THUMB_W + GAP), PAD + r * (THUMB_H + GAP)
        sheet.paste(im, (x, y))
        if label:
            draw.rectangle(
                [x, y + THUMB_H - 14, x + THUMB_W, y + THUMB_H], fill=(0, 0, 0)
            )
            draw.text(
                (x + 3, y + THUMB_H - 13),
                os.path.basename(p)[:28],
                fill=(255, 255, 255),
                font=font,
            )
    sheet.save(out)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "targets", nargs="+", help="截图文件或目录（目录收 png/jpg/webp/gif）"
    )
    ap.add_argument("-o", "--output", required=True, help="输出 .html 或 .png")
    ap.add_argument(
        "--cols", type=int, default=6, help="PNG 模式列数（默认 6；HTML flex 自适应）"
    )
    ap.add_argument(
        "--label", action="store_true", help="缩略图叠加文件名标签（目检定位用）"
    )
    args = ap.parse_args()

    if args.cols < 1:
        print("FAIL --cols 必须 ≥1", file=sys.stderr)
        sys.exit(2)
    paths = collect(args.targets)
    if not paths:
        print("FAIL 无图片输入", file=sys.stderr)
        sys.exit(2)
    out = args.output
    ext = os.path.splitext(out)[1].lower()
    if ext not in (".html", ".png"):
        print(f"FAIL 输出后缀不支持: {ext}（仅 .html / .png）", file=sys.stderr)
        sys.exit(2)

    d = os.path.dirname(os.path.abspath(out))
    os.makedirs(d, exist_ok=True)

    if ext == ".png":
        if build_png(paths, out, args.cols, args.label):
            kb = os.path.getsize(out) / 1024
            print(
                f"[OK] contact-sheet {out}: {len(paths)} 张缩略图, {args.cols} 列, "
                f"{kb:.0f}KB（PNG 合成, 几何 160×90/gap8/pad16/#808080）"
            )
            sys.exit(0)
        fallback = os.path.splitext(out)[0] + ".html"
        print(
            f"[WARN] pillow-missing 未装 Pillow，PNG 合成不可用 → 降级输出 {fallback}"
            f"（HTML 并排表恒可出，浏览器打开同样目检）"
        )
        out = fallback
    try:
        with open(out, "w", encoding="utf-8") as f:
            f.write(build_html(paths, args.label))
    except OSError as e:
        print(f"FAIL 写入失败 {out}: {e}", file=sys.stderr)
        sys.exit(2)
    kb = os.path.getsize(out) / 1024
    print(
        f"[OK] contact-sheet {out}: {len(paths)} 张缩略图 base64 内联, {kb:.0f}KB"
        f"（审查工具，不进交付物；目检三件事见 camera-storyboard.md §14）"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
