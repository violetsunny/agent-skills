#!/usr/bin/env python3
"""字节级验证：PPTX 内嵌媒体 md5 与源图目录逐一比对（标准库 zipfile+hashlib）。

契约来源: references/phase5-ppt-delivery.md:305-311（无 LibreOffice 环境的替代目检第 2 条）。

用法:
  python3 verify_media_md5.py <deck.pptx> <源图目录> [--media-only]

判定:
  1. ppt/media/ 每个文件的 md5 必须能在源图目录中找到相同 md5（未被替换降质）
  2. 源图目录每个图片文件的 md5 必须已嵌入 ppt/media/（图片未丢失）；
     --media-only 时跳过本方向（源目录含非交付图时使用）

假设（md 未明确，按契约精神决定）:
  - 源图目录递归扫描，只认图片扩展名 .png/.jpg/.jpeg/.gif/.bmp/.tiff/.webp/.emf/.wmf
  - md5 相同即视为同一文件（契约即 md5 口径），不比文件名
"""

import argparse
import hashlib
import os
import sys
import zipfile

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".emf", ".wmf")


def md5_bytes(data):
    return hashlib.md5(data).hexdigest()


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description="ppt/media 与源图目录 md5 逐一比对")
    ap.add_argument("pptx")
    ap.add_argument("srcdir", help="源截图/图表 PNG 目录")
    ap.add_argument(
        "--media-only",
        action="store_true",
        help="只校验 media→源 方向（不要求源图全部嵌入）",
    )
    args = ap.parse_args()

    if not os.path.isdir(args.srcdir):
        print(f"FAIL 源图目录不存在: {args.srcdir}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(args.pptx) as zf:
        media = {}
        for name in zf.namelist():
            if name.startswith("ppt/media/") and not name.endswith("/"):
                media[name] = md5_bytes(zf.read(name))

    src = {}
    for root, _dirs, files in os.walk(args.srcdir):
        for fn in sorted(files):
            if fn.lower().endswith(IMAGE_EXTS):
                p = os.path.join(root, fn)
                src[p] = md5_file(p)

    if not media:
        print("FAIL pptx 内无 ppt/media/ 媒体文件", file=sys.stderr)
        return 1

    src_by_md5 = {}
    for p, m in src.items():
        src_by_md5.setdefault(m, []).append(p)
    media_by_md5 = {}
    for n, m in media.items():
        media_by_md5.setdefault(m, []).append(n)

    fails = []
    for name, m in sorted(media.items()):
        if m in src_by_md5:
            print(f"[ OK ] {name} md5={m} == {src_by_md5[m][0]}")
        else:
            fails.append(f"{name} md5={m} 在源图目录无匹配（疑似被替换/降质）")

    if not args.media_only:
        for p, m in sorted(src.items()):
            if m not in media_by_md5:
                fails.append(f"{p} md5={m} 未嵌入 ppt/media/（图片丢失）")

    if fails:
        print("FAIL md5 比对不通过:")
        for f in fails:
            print("  -", f)
        return 1
    print(f"PASS media {len(media)} 个 / 源图 {len(src)} 个，md5 比对通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
