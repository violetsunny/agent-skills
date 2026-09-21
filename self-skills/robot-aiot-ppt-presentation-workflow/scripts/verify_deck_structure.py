#!/usr/bin/env python3
"""交付后结构验证：PPTX 页数 + 每页标题与母稿 MD 比对（标准库 zipfile+xml.etree 解析）。

契约来源: references/phase5-ppt-delivery.md「交付后验证·结构验证」第 1/2 条。

用法:
  python3 verify_deck_structure.py <deck.pptx> <母稿.md>

判定:
  1. 页数一致: PPTX 幻灯片数 == 母稿页标记数（`## Page N` 或 `## 第 N 页`）
  2. 每页标题一致: 归一化（去空白与 markdown 记号）后相等 → OK；
     单向包含 → WARN；否则 FAIL

假设（md 未明确，按契约精神决定）:
  - 页序: 按 presentation.xml sldIdLst + rels 解析真实放映顺序
  - 标题提取: 优先 title/ctrTitle 占位符；无占位符时取该页文档序第一个非空文本
  - 母稿标题: `### 标题` 小节首个非空行；缺失时回退 `## Page N: 类型 — 标题` 破折号后文本
"""

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PAGE_RE = re.compile(r"^##\s*(?:Page|第)\s*(\d+)\s*页?\s*[:：]?\s*(.*)$", re.M | re.I)
MD_STRIP_RE = re.compile(r"[*`#>]")


def norm(s):
    return MD_STRIP_RE.sub("", re.sub(r"\s+", "", s or ""))


def slide_order(zf):
    """按放映顺序返回 slide part 名列表。"""
    pres = ET.fromstring(zf.read("ppt/presentation.xml"))
    rels = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
    rid2target = {rel.get("Id"): rel.get("Target") for rel in rels}
    order = []
    for sld_id in pres.iter(f"{NS_P}sldId"):
        target = rid2target.get(sld_id.get(f"{NS_R}id"), "")
        name = target.lstrip("/")
        if not name.startswith("ppt/"):
            name = "ppt/" + name
        order.append(name)
    return order


def slide_title(zf, part):
    root = ET.fromstring(zf.read(part))
    fallback = None
    for sp in root.iter(f"{NS_P}sp"):
        texts = [t.text or "" for t in sp.iter(f"{NS_A}t")]
        joined = "".join(texts).strip()
        if not joined:
            continue
        ph = sp.find(f"{NS_P}nvSpPr/{NS_P}nvPr/{NS_P}ph")
        if ph is not None and ph.get("type") in ("title", "ctrTitle"):
            return joined
        if fallback is None:
            fallback = joined
    return fallback or ""


def parse_md_titles(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    matches = list(PAGE_RE.finditer(src))
    pages = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(src)
        block = src[m.end() : end]
        title = ""
        sec = re.search(r"^###\s*标题\s*$(.*?)(?=^###|\Z)", block, re.M | re.S)
        if sec:
            for line in sec.group(1).splitlines():
                if line.strip():
                    title = line.strip()
                    break
        if not title:
            heading = m.group(2)
            for dash in ("—", "──", " - "):
                if dash in heading:
                    heading = heading.split(dash)[-1]
                    break
            title = heading.strip()
        pages.append((int(m.group(1)), title))
    return pages


def main():
    ap = argparse.ArgumentParser(description="PPTX 页数与每页标题 vs 母稿 MD")
    ap.add_argument("pptx")
    ap.add_argument("md", help="母稿 MD 路径")
    args = ap.parse_args()

    with zipfile.ZipFile(args.pptx) as zf:
        order = slide_order(zf)
        deck_titles = [slide_title(zf, part) for part in order]
    md_pages = parse_md_titles(args.md)

    fails = []
    if not md_pages:
        print("FAIL 母稿中未解析到 `## Page N` / `## 第 N 页` 页标记", file=sys.stderr)
        return 1

    print(f"PPTX 页数: {len(deck_titles)}  母稿页数: {len(md_pages)}")
    if len(deck_titles) != len(md_pages):
        fails.append(f"页数不一致: PPTX {len(deck_titles)} vs 母稿 {len(md_pages)}")

    for i, (page_no, md_title) in enumerate(md_pages):
        if i >= len(deck_titles):
            break
        deck_t = deck_titles[i]
        a, b = norm(deck_t), norm(md_title)
        if a == b:
            print(f"[ OK ] 页{page_no}: {deck_t}")
        elif a and b and (a in b or b in a):
            print(
                f"[WARN] 页{page_no}: 标题包含不一致 PPTX={deck_t!r} 母稿={md_title!r}"
            )
        else:
            fails.append(f"页{page_no}: 标题不一致 PPTX={deck_t!r} 母稿={md_title!r}")

    if fails:
        print("FAIL 结构验证不通过:")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS 页数与每页标题验证通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
