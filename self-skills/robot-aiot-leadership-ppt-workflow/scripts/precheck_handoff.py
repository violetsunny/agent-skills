#!/usr/bin/env python3
"""移交 ppt-master 前校验（机判子集）。

契约来源: references/phase5-ppt-delivery.md:5-16（移交前校验）、:24-38（调用输入清单）。

用法:
  python3 precheck_handoff.py <工作目录>            # 工作目录即 doc-ppt/
  python3 precheck_handoff.py doc-ppt --skip-logo   # 甲方模板继承路线跳过 logo 校验(phase5「甲方模板继承」继承规则 3)

机判项:
  1. 零宽字符扫描（.md/.html/.xml/.css/.js/.svg/.txt 中的不可见字符）  → 校验第 3 条
  2. Markdown 表格列数与分隔行一致                                      → 校验第 4 条
  3. flow/ 图表 XML ↔ HTML 文件配对                                     → 校验第 5 条
  4. pages/*.html 页数与母稿 `## Page N` 标记数对齐                     → 校验第 6/7 条
  5. assets/midea-logo.png 就位                                         → 校验第 9 条
  6. 输入清单存在性: 母稿 MD / flow/ / pages/ / logo                    → :24-30

假设（md 未明确，按契约精神决定）:
  - 母稿识别: 工作目录下 glob `*母稿*.md`，取第一个
  - 页数标记: 母稿中 `^## Page N` 行（与 phase2-pagination.md 母稿模板一致）
  - 零宽字符集: U+200B/200C/200D/200E/200F/2060/FEFF/00AD
  - 数据一致性/四要素/配色体系等语义项不可机判，不在本脚本范围
"""

import argparse
import glob
import os
import re
import sys

ZERO_WIDTH = {
    "\u200b": "ZWSP",
    "\u200c": "ZWNJ",
    "\u200d": "ZWJ",
    "\u200e": "LRM",
    "\u200f": "RLM",
    "\u2060": "WJ",
    "\ufeff": "BOM",
    "\u00ad": "SHY",
}
TEXT_EXTS = (".md", ".html", ".xml", ".css", ".js", ".svg", ".txt")
PAGE_MARK_RE = re.compile(r"^##\s*Page\s*\d+", re.M | re.I)
SEP_ROW_RE = re.compile(r"^[\s|:\-]+$")


def col_count(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return len(s.split("|"))


def check_zero_width(workdir, findings):
    for root, dirs, files in os.walk(workdir):
        dirs[:] = [d for d in dirs if d not in ("assets", ".git", "node_modules")]
        for name in sorted(files):
            if not name.endswith(TEXT_EXTS):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as f:
                    lines = f.read().splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for ln, line in enumerate(lines, 1):
                for ch, label in ZERO_WIDTH.items():
                    if ch in line:
                        findings.append(
                            ("FAIL", f"{path}:{ln}: 零宽字符 {label} U+{ord(ch):04X}")
                        )


def check_md_tables(workdir, findings):
    for root, dirs, files in os.walk(workdir):
        dirs[:] = [d for d in dirs if d not in ("assets", ".git", "node_modules")]
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
            i = 0
            while i < len(lines):
                if not lines[i].lstrip().startswith("|"):
                    i += 1
                    continue
                block = []
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    block.append((i + 1, lines[i]))
                    i += 1
                if len(block) < 2:
                    continue
                sep = block[1][1].strip()
                if "-" not in sep or not SEP_ROW_RE.match(sep):
                    findings.append(
                        (
                            "WARN",
                            f"{path}:{block[0][0]}: 表格块第 2 行不是分隔行，跳过列数校验",
                        )
                    )
                    continue
                ncol = col_count(sep)
                for ln, row in block:
                    c = col_count(row)
                    if c != ncol:
                        findings.append(
                            (
                                "FAIL",
                                f"{path}:{ln}: 表格列数 {c} 与分隔行 {ncol} 不一致",
                            )
                        )


def check_flow_pairing(workdir, findings):
    flow = os.path.join(workdir, "flow")
    if not os.path.isdir(flow):
        findings.append(("WARN", f"{flow}: 目录不存在（本 deck 无图表则忽略）"))
        return
    xmls = sorted(glob.glob(os.path.join(flow, "*.xml")))
    htmls = {
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(flow, "*.html"))
    }
    for x in xmls:
        stem = os.path.splitext(os.path.basename(x))[0]
        if stem not in htmls:
            findings.append(("FAIL", f"{x}: 图表 XML 无对应 HTML（phase5:11）"))
    xml_stems = {os.path.splitext(os.path.basename(p))[0] for p in xmls}
    for h in sorted(htmls - xml_stems):
        findings.append(("WARN", f"{flow}/{h}.html: 无对应 XML 真源"))


def check_page_alignment(workdir, md_path, findings):
    pages_dir = os.path.join(workdir, "pages")
    if not os.path.isdir(pages_dir):
        findings.append(("FAIL", f"{pages_dir}: 目录不存在（phase5:29 输入清单）"))
        return
    htmls = sorted(glob.glob(os.path.join(pages_dir, "*.html")))
    if not htmls:
        findings.append(
            ("FAIL", f"{pages_dir}: 无 .html，页面 HTML 未生成（phase5:13）")
        )
        return
    if md_path is None:
        findings.append(("WARN", "未找到母稿 MD，无法做页数对齐"))
        return
    with open(md_path, encoding="utf-8") as f:
        marks = PAGE_MARK_RE.findall(f.read())
    if not marks:
        findings.append(
            ("WARN", f"{md_path}: 未见 `## Page N` 页标记，无法机判页数对齐")
        )
        return
    if len(htmls) != len(marks):
        findings.append(
            (
                "FAIL",
                f"页数不对齐: pages/*.html {len(htmls)} 页 vs 母稿 {len(marks)} 页",
            )
        )
    else:
        findings.append(("OK", f"页数对齐: {len(htmls)} 页"))


def check_inputs(workdir, skip_logo, findings):
    mds = sorted(glob.glob(os.path.join(workdir, "*母稿*.md")))
    if not mds:
        findings.append(("FAIL", f"{workdir}: 未找到母稿 MD（*母稿*.md，phase5:26）"))
        return None
    findings.append(("OK", f"母稿: {mds[0]}"))
    logo = os.path.join(workdir, "assets", "midea-logo.png")
    if skip_logo:
        findings.append(
            ("OK", "甲方模板继承路线，跳过 midea-logo.png 校验（phase5「甲方模板继承」继承规则 3）")
        )
    elif os.path.isfile(logo):
        findings.append(("OK", f"logo 就位: {logo}"))
    else:
        findings.append(("FAIL", f"{logo}: 未就位（phase5:15,30）"))
    return mds[0]


def main():
    ap = argparse.ArgumentParser(description="移交 ppt-master 前校验（机判子集）")
    ap.add_argument("workdir", help="工作目录（doc-ppt/）")
    ap.add_argument(
        "--skip-logo", action="store_true", help="甲方模板继承路线跳过 logo 校验"
    )
    args = ap.parse_args()

    if not os.path.isdir(args.workdir):
        print(f"FAIL {args.workdir} 不是目录", file=sys.stderr)
        return 2

    findings = []
    md_path = check_inputs(args.workdir, args.skip_logo, findings)
    check_zero_width(args.workdir, findings)
    check_md_tables(args.workdir, findings)
    check_flow_pairing(args.workdir, findings)
    check_page_alignment(args.workdir, md_path, findings)

    n_fail = n_warn = 0
    for level, msg in findings:
        if level == "FAIL":
            n_fail += 1
            print("[FAIL]", msg)
        elif level == "WARN":
            n_warn += 1
            print("[WARN]", msg)
        else:
            print("[ OK ]", msg)
    print(f"--- precheck 汇总: FAIL={n_fail}, WARN={n_warn} ---")
    if n_fail:
        print("FAIL 移交前校验不通过，修正后再调用 ppt-master")
        return 1
    print("PASS 机判子项全过（语义项仍需人工/sub agent 校验）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
