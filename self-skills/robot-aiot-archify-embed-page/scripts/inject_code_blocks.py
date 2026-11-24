#!/usr/bin/env python3
"""<!--BLOCK:key--> 标记 → verbatim 代码块注入（HTML 转义 + 脱敏），保证字节保真替代手打。

blocks.json: {key: {"start": N, "end": N, "lang": "java", "label": "Foo.java"}}
——源文件 1-indexed 闭区间行号（行号基于 clean_export_md.py 产出的 === SOURCE: 拼接文本）。
项目专属展开逻辑（字段表→JSON 等）不内置：预渲染成文本追加进 sources.txt 后按普通 block 注册。
剩余标记 → exit 1（失败可见，禁静默留标记）。

用法: python3 inject_code_blocks.py <page.html> <sources.txt> <blocks.json>
      [--mask-regex 'sk-[A-Za-z0-9]+'] [--mask-to sk-xxx]
仅 stdlib。
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path


def clean(text, mask_re, mask_to):
    # 只 pop 尾部空行与 ~ 占位行，绝不 strip 内容字符——
    # 默认 strip 会吃掉 U+001F 分隔符（Python 视 U+001C–001F 为空白），判空一律 strip(" \t")
    out = text.split("\n")
    while out and not out[-1].strip(" \t"):
        out.pop()
    while out and out[-1].strip(" \t") == "~":
        out.pop()
    while out and not out[-1].strip(" \t"):
        out.pop()
    body = "\n".join(out)
    body = mask_re.sub(mask_to, body)
    assert "\ufeff" not in body and "\u200b" not in body
    return body


def render(lang, label, body):
    return (
        '<div class="codeblock">\n'
        f'        <div class="code-head"><span class="lang-tag">{lang}</span>'
        f'<span class="file-path">{html.escape(label)}</span></div>\n'
        f"        <pre><code>{html.escape(body)}</code></pre>\n"
        "      </div>"
    )


def main():
    ap = argparse.ArgumentParser(description="verbatim 代码块注入（HTML 转义 + 脱敏）")
    ap.add_argument("page")
    ap.add_argument("sources")
    ap.add_argument("blocks")
    ap.add_argument("--mask-regex", default=r"sk-[A-Za-z0-9]+")
    ap.add_argument("--mask-to", default="sk-xxx")
    args = ap.parse_args()
    page_path = Path(args.page)
    lines = Path(args.sources).read_text(encoding="utf-8").split("\n")
    blocks = json.loads(Path(args.blocks).read_text(encoding="utf-8"))
    mask_re = re.compile(args.mask_regex)
    page = page_path.read_text(encoding="utf-8")
    used = set()
    for key, spec in blocks.items():
        marker = f"<!--BLOCK:{key}-->"
        if marker not in page:
            continue
        a, b = spec["start"], spec["end"]
        body = clean("\n".join(lines[a - 1 : b]), mask_re, args.mask_to)
        page = page.replace(marker, render(spec["lang"], spec["label"], body))
        used.add(key)
    left = re.findall(r"<!--BLOCK:([A-Za-z0-9_-]+)-->", page)
    unused = [k for k in blocks if k not in used]
    page_path.write_text(page, encoding="utf-8")
    print(f"injected {len(used)} blocks; remaining markers: {left}")
    if unused:
        print(f"registered but no marker in page: {unused}")
    print(f"page lines: {len(page.split(chr(10)))}")
    if left:
        sys.exit(1)


if __name__ == "__main__":
    main()
