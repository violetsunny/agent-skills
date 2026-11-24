#!/usr/bin/env python3
"""云效 Thoughts 导出 md 噪声清洗 → 可逐字转录纯文本（references/rebuild-mode.md §2 配方）。

清理项（均为导出噪声，非原文内容）：
  - BOM / 零宽字符（\ufeff \u200b）
  - 代码围栏闭合前一行单独成行的语言标签（lines[-2]，不是 lines[-1]）
  - 「##### ✅标题 + 截断摘要 + 品牌词」链接卡片预览——须 --card-brand 指定品牌词才剔除；
    不指定则不动（无品牌锚点的通用正则会误吞真实 ✅ 小节内容）
  - UI 噪声（no-search-result.png / 「你可以将零散的思绪与文字先整理为草稿」文案，云效导出工具特性）
  - 全部图片 → [IMG] 占位（--keep-images 保留；全站惯例不嵌远程截图，CDN 图占位后重表达）
代码围栏内内容不动（re.split 保护）。多文件拼接保留 === SOURCE: 分隔头
（inject_code_blocks.py 的行号定位依赖它）。

用法: python3 clean_export_md.py <out.txt> <md路径>... [--card-brand BRAND] [--keep-images]
仅 stdlib。
"""

import argparse
import re
import sys

LANG_TAGS = {
    "Plain Text",
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "JSON",
    "YAML",
    "XML",
    "HTML",
    "CSS",
    "SQL",
    "Bash",
    "Shell",
    "Go",
    "Rust",
    "C",
    "C++",
    "Text",
    "Markdown",
    "Properties",
    "Toml",
    "INI",
    "Diff",
    "Groovy",
    "Kotlin",
}
UI_NOISE = [
    "你可以将零散的思绪与文字先整理为草稿",
    "https://g.alicdn.com/aone-tb/thoughts-front/images/no-search-result",
]


def clean(text, card_re, keep_images):
    text = text.replace("\ufeff", "").replace("\u200b", "")
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("```"):
            lines = p.split("\n")
            while len(lines) > 2 and lines[-1].strip() == "":
                lines.pop()
            if len(lines) > 2 and lines[-1].strip() == "```":
                while len(lines) > 2 and lines[-2].strip() == "":
                    del lines[-2]
                if len(lines) > 2 and lines[-2].strip() in LANG_TAGS:
                    del lines[-2]
            out.append("\n".join(lines))
        else:
            if card_re:
                p = card_re.sub("", p)
            if not keep_images:
                p = re.sub(r"!\[[^\]]*\]\([^)]*\)", "[IMG]", p)
            for noise in UI_NOISE:
                p = "\n".join(ln for ln in p.split("\n") if noise not in ln)
            out.append(p)
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="云效 Thoughts 导出 md 噪声清洗")
    ap.add_argument("out")
    ap.add_argument("srcs", nargs="+")
    ap.add_argument(
        "--card-brand", default=None, help="卡片预览终止品牌词；不指定则不剔除卡片"
    )
    ap.add_argument("--keep-images", action="store_true")
    args = ap.parse_args()
    card_re = (
        re.compile(
            r"#####\s*✅[^\n]*\n(?:[^\n]*\n)*?" + re.escape(args.card_brand) + r"\s*\n"
        )
        if args.card_brand
        else None
    )
    chunks = []
    for s in args.srcs:
        with open(s, encoding="utf-8") as fh:
            raw = fh.read()
        body = clean(raw, card_re, args.keep_images)
        chunks.append(f"\n\n{'=' * 78}\n=== SOURCE: {s}\n{'=' * 78}\n{body}")
        print(f"{s}: raw={len(raw)} clean={len(body)}")
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("".join(chunks))
    print(f"written {args.out}")


if __name__ == "__main__":
    sys.exit(main())
