#!/usr/bin/env python3
"""PPT 演示工作流每环节交接（handoff）校验 + 落盘。

每个 Phase 结束时跑本脚本：校验本环节产物存在、确认门状态已记录、下一环节
输入齐备；FAIL 阻塞，不得进入下一环节。--write 落盘 _gen/handoff-phaseN.md
交接记录（产物清单/确认门/机检结果自动填，遗留风险待主线程补）。

与 precheck_handoff.py 的分工（互补，不重复）:
  - check_phase_handoff.py : 环节间交接（Phase 1/2/3/3.5/4），校验本环节产物 +
    确认门状态 + 下一环节输入齐备
  - precheck_handoff.py    : Phase 5 移交 ppt-master 前的最终校验（零宽字符/表格
    GFM/flow 配对/页数对齐/logo/输入清单）；Phase 5 的交接即 precheck_handoff.py，
    本脚本不含 --phase 5

契约来源:
  SKILL.md 各 Phase「交接(handoff)」节、references/phase*-*.md 交接节、
  templates/ppt-manuscript.md（母稿头部确认状态/风格基准字段、图表需求总表表头）、
  references/phase1-source-analysis.md（数据池产物）。

用法:
  python3 check_phase_handoff.py <workdir> --phase N          # 校验，FAIL 阻塞
  python3 check_phase_handoff.py <workdir> --phase N --write  # 校验并落盘交接记录
  # workdir = doc-ppt/ 或用户指定输出目录；N ∈ 1/2/3/3.5/4

环节契约（PPT 5 阶段，Phase 5 走 precheck_handoff.py）:
  Phase 1→2  : 数据池 MD 存在（*数据池.md，含数据项表）
  Phase 2→3  : 母稿存在（*母稿*.md）+ G1 已通过 + 图表需求总表章节存在
  Phase 3→3.5: flow/ XML 真源存在（*.xml）
  Phase 3.5→4: flow/ XML↔HTML 配对（桥接产物 *.html）+ G2 已通过
  Phase 4→5  : 母稿回写完整（图表需求总表类型非「无」行的产物路径指向存在的 flow
               文件、确认状态列已填）+ pages/*.html 存在 + showcase 门已过（风格基准已锁定）

确认门机检口径: 只校验母稿头部「确认状态」字段已标记「已通过」、「风格基准」字段
已锁定（非占位符/非「待锁定」），不替代用户语义确认（与 precheck_handoff.py
「语义项仍需人工」口径一致）。

假设（md 未明确，按契约精神决定）:
  - 母稿识别: workdir 下 *母稿*.md，取第一个（与 precheck_handoff.py 同 glob）
  - 数据池识别: workdir 下 *数据池.md，取第一个
  - 确认状态字段: 母稿头部 `确认状态：...`；含尖括号占位符视为未填充→门未通过
  - 风格基准字段: 母稿头部 `风格基准：...`；含尖括号占位符或「待锁定」→showcase 门未过
  - 图表需求总表: `## 图表需求总表` 章节下第一个表格，表头 7 列
    （# / 页面 / 图表名 / 类型 / 核心信息 / 产物路径 / 确认状态）
"""

import argparse
import glob
import os
import re
import sys
from datetime import datetime

CONFIRM_RE = re.compile(r"确认状态[:：]\s*(.+)")
STYLE_RE = re.compile(r"风格基准[:：]\s*(.+)")
CHART_TABLE = "图表需求总表"
FLOW_PATH_RE = re.compile(r"flow/[^\s，,；;+]*?\.(?:xml|html)")
DATA_POOL_MARK = "数据项"
PHASE_NAMES = {
    "1": "Phase 1 源文件分析（数据池+反问）",
    "2": "Phase 2 PPT演示母稿",
    "3": "Phase 3 图表 XML 真源",
    "3.5": "Phase 3.5 XML→HTML 桥接",
    "4": "Phase 4 回写母稿+逐页 HTML",
}


def find_manuscript(workdir):
    mds = sorted(glob.glob(os.path.join(workdir, "*母稿*.md")))
    return mds[0] if mds else None


def find_data_pool(workdir):
    ps = sorted(glob.glob(os.path.join(workdir, "*数据池.md")))
    return ps[0] if ps else None


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        return ""


def parse_field(md_path, regex):
    """母稿头部某字段原文；无母稿或无字段返回 None。"""
    if not md_path:
        return None
    for line in read_text(md_path).splitlines():
        m = regex.search(line)
        if m:
            return m.group(1).strip()
    return None


def parse_confirm(md_path):
    return parse_field(md_path, CONFIRM_RE)


def parse_style_basis(md_path):
    return parse_field(md_path, STYLE_RE)


def gate_passed(confirm_text, gate):
    """确认状态字段是否标记某门（G1/G2）已通过。占位符（含尖括号）视为未填充。"""
    if not confirm_text:
        return False
    if "<" in confirm_text and ">" in confirm_text:
        return False
    m = re.search(rf"{gate}\s*(已通过|待确认)", confirm_text)
    return m is not None and m.group(1) == "已通过"


def style_basis_locked(style_text):
    """风格基准字段是否已锁定（showcase 门已过）。占位符或「待锁定」视为未过。"""
    if not style_text:
        return False
    if "<" in style_text and ">" in style_text:
        return False
    if "待锁定" in style_text:
        return False
    return True


def section_exists(text, title):
    return re.search(rf"^##\s+{re.escape(title)}", text, re.M) is not None


def table_rows_after(text, section_title):
    """某章节下第一个表格的数据行（cell 列表）；章节不存在返回 None，无数据行返回 []。"""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^##\s+{re.escape(section_title)}", line):
            start = i + 1
            break
    if start is None:
        return None
    rows = []
    in_table = False
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("|"):
            in_table = True
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
        elif s.startswith("##"):
            break
        elif in_table:
            break
    return rows[1:] if rows else []


def check_phase1(workdir, findings):
    dp = find_data_pool(workdir)
    if not dp:
        findings.append(
            ("FAIL", f"{workdir}: 未找到数据池 MD（*数据池.md，Phase 1 产物）")
        )
        return
    findings.append(("OK", f"数据池: {dp}"))
    text = read_text(dp)
    if DATA_POOL_MARK in text:
        findings.append(("OK", "数据池含数据项表（下一环节输入：母稿数据引用源）"))
    else:
        findings.append(
            ("WARN", f"{dp}: 未见「{DATA_POOL_MARK}」表头，确认数据池表已填充")
        )


def check_phase2(workdir, findings):
    md = find_manuscript(workdir)
    if not md:
        findings.append(("FAIL", f"{workdir}: 未找到 PPT 母稿（*母稿*.md）"))
        return
    findings.append(("OK", f"母稿: {md}"))
    text = read_text(md)
    confirm = parse_confirm(md)
    if gate_passed(confirm, "G1"):
        findings.append(("OK", f"G1 已通过（确认状态：{confirm}）"))
    else:
        findings.append(
            (
                "FAIL",
                f"G1 未通过（确认状态：{confirm or '缺字段'}）；"
                "须用户确认母稿「不需要调整」后更新头部确认状态为「G1 已通过（日期）」",
            )
        )
    if section_exists(text, CHART_TABLE):
        rows = table_rows_after(text, CHART_TABLE)
        if rows:
            findings.append(
                (
                    "OK",
                    f"图表需求总表存在（{len(rows)} 行，下一环节输入：图表 XML 生成清单）",
                )
            )
        else:
            findings.append(
                ("WARN", "图表需求总表无数据行（本 deck 无图表则正常，Phase 3 可跳过）")
            )
    else:
        findings.append(("FAIL", f"母稿缺「{CHART_TABLE}」章节"))


def check_phase3(workdir, findings):
    flow = os.path.join(workdir, "flow")
    if not os.path.isdir(flow):
        findings.append(("FAIL", f"{flow}: 目录不存在（Phase 3 图表 XML 落 flow/）"))
        return
    xmls = sorted(glob.glob(os.path.join(flow, "*.xml")))
    if not xmls:
        findings.append(
            ("WARN", f"{flow}: 无 XML（本 deck 无图表则正常，下一环节输入：桥接源）")
        )
    else:
        findings.append(
            (
                "OK",
                f"flow/ XML 真源存在（{len(xmls)} 张，下一环节输入：XML→HTML 桥接源）",
            )
        )


def check_phase3_5(workdir, findings):
    flow = os.path.join(workdir, "flow")
    if not os.path.isdir(flow):
        findings.append(("FAIL", f"{flow}: 目录不存在（Phase 3.5 桥接产物落 flow/）"))
        return
    xmls = sorted(glob.glob(os.path.join(flow, "*.xml")))
    htmls = {
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(flow, "*.html"))
    }
    if not xmls:
        findings.append(("WARN", f"{flow}: 无 XML（本 deck 无图表则正常）"))
    unpaired = 0
    for x in xmls:
        stem = os.path.splitext(os.path.basename(x))[0]
        if stem not in htmls:
            findings.append(("FAIL", f"{x}: XML 无对应 HTML（桥接产物缺失）"))
            unpaired += 1
    xml_stems = {os.path.splitext(os.path.basename(p))[0] for p in xmls}
    for h in sorted(htmls - xml_stems):
        findings.append(("WARN", f"{flow}/{h}.html: 无对应 XML 真源"))
    if xmls and not unpaired:
        findings.append(
            (
                "OK",
                f"flow/ XML↔HTML 配对（{len(xmls)} 张，下一环节输入：页面引用图表 HTML）",
            )
        )
    md = find_manuscript(workdir)
    confirm = parse_confirm(md)
    if gate_passed(confirm, "G2"):
        findings.append(("OK", f"G2 已通过（确认状态：{confirm}）"))
    else:
        findings.append(
            (
                "FAIL",
                f"G2 未通过（确认状态：{confirm or '缺字段/无母稿'}）；"
                "须用户确认图表无误后更新母稿头部确认状态为「G2 已通过（日期）」",
            )
        )


def check_phase4(workdir, findings):
    md = find_manuscript(workdir)
    if not md:
        findings.append(("FAIL", f"{workdir}: 未找到 PPT 母稿"))
        return
    text = read_text(md)

    rows = table_rows_after(text, CHART_TABLE)
    if rows is None:
        findings.append(("FAIL", f"母稿缺「{CHART_TABLE}」章节"))
    else:
        chart_rows = [r for r in rows if len(r) >= 7 and r[3] and r[3] != "无"]
        if not chart_rows:
            findings.append(("OK", "图表需求总表无需图表行（回写校验跳过）"))
        else:
            incomplete = []
            for r in chart_rows:
                rid, path_col, confirm_col = r[0], r[5], r[6]
                if not path_col:
                    incomplete.append(f"{rid}(产物路径空)")
                    continue
                if not confirm_col:
                    incomplete.append(f"{rid}(确认状态空)")
                for token in FLOW_PATH_RE.findall(path_col):
                    if not os.path.isfile(os.path.join(workdir, token)):
                        incomplete.append(f"{rid}(路径不存在:{token})")
            if incomplete:
                findings.append(
                    (
                        "FAIL",
                        f"图表需求总表回写不完整: {incomplete}"
                        "（类型非「无」行的产物路径须指向存在的 flow 文件、确认状态列须填）",
                    )
                )
            else:
                findings.append(
                    (
                        "OK",
                        f"图表需求总表回写完整（{len(chart_rows)} 行图表，产物路径+确认状态齐备）",
                    )
                )

    pages = os.path.join(workdir, "pages")
    if not os.path.isdir(pages):
        findings.append(("FAIL", f"{pages}: 目录不存在（Phase 4 逐页 HTML 落 pages/）"))
    else:
        htmls = sorted(glob.glob(os.path.join(pages, "*.html")))
        if not htmls:
            findings.append(("FAIL", f"{pages}: 无 .html，逐页 HTML 未生成"))
        else:
            findings.append(
                (
                    "OK",
                    f"pages/ 逐页 HTML 存在（{len(htmls)} 页，下一环节输入：ppt-master 视觉源）",
                )
            )

    style = parse_style_basis(md)
    if style_basis_locked(style):
        findings.append(("OK", f"showcase 门已过（风格基准：{style}）"))
    else:
        findings.append(
            (
                "FAIL",
                f"showcase 门未过（风格基准：{style or '缺字段'}）；"
                "须两页 showcase 经用户确认后把风格基准写入母稿头部（非占位符/非「待锁定」）",
            )
        )


def write_handoff(workdir, phase, findings):
    gen = os.path.join(workdir, "_gen")
    os.makedirs(gen, exist_ok=True)
    path = os.path.join(gen, f"handoff-phase{phase}.md")
    n_fail = sum(1 for lv, _ in findings if lv == "FAIL")
    n_warn = sum(1 for lv, _ in findings if lv == "WARN")
    verdict = "FAIL（阻塞，不得进入下一环节）" if n_fail else "PASS（可进入下一环节）"
    md = find_manuscript(workdir)
    confirm = parse_confirm(md) or "（母稿未生成或无确认状态字段）"
    style = parse_style_basis(md) or "（母稿未生成或无风格基准字段）"
    result_lines = "\n".join(f"- [{lv}] {msg}" for lv, msg in findings)
    content = (
        f"# Phase {phase} 交接记录（handoff）\n\n"
        f"- 环节：{PHASE_NAMES.get(phase, phase)}\n"
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- 工作目录：{workdir}\n\n"
        f"## 确认门状态\n{confirm}\n\n"
        f"## 风格基准（showcase 门）\n{style}\n\n"
        f"## 机检结果（check_phase_handoff.py --phase {phase}）\n"
        f"判定：{verdict}｜FAIL={n_fail} WARN={n_warn}\n\n"
        f"{result_lines}\n\n"
        f"## 下一环节输入齐备性\n"
        f"见上「机检结果」；FAIL=0 即齐备，可进入下一环节。\n\n"
        f"## 遗留风险 / 待办\n"
        f"<主线程补充：本环节未尽事项、需下一环节注意的风险；无则写「无」>\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


ROUTER = {
    "1": check_phase1,
    "2": check_phase2,
    "3": check_phase3,
    "3.5": check_phase3_5,
    "4": check_phase4,
}


def main():
    ap = argparse.ArgumentParser(
        description="PPT 演示工作流每环节交接（handoff）校验 + 落盘"
    )
    ap.add_argument("workdir", help="工作目录（doc-ppt/ 或用户指定输出目录）")
    ap.add_argument(
        "--phase", required=True, choices=sorted(ROUTER), help="环节编号（1/2/3/3.5/4）"
    )
    ap.add_argument(
        "--write", action="store_true", help="落盘 _gen/handoff-phaseN.md 交接记录"
    )
    args = ap.parse_args()

    if not os.path.isdir(args.workdir):
        print(f"FAIL {args.workdir} 不是目录", file=sys.stderr)
        return 2

    findings = []
    ROUTER[args.phase](args.workdir, findings)

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
    print(f"--- handoff Phase {args.phase} 汇总: FAIL={n_fail}, WARN={n_warn} ---")

    if args.write:
        p = write_handoff(args.workdir, args.phase, findings)
        print(f"交接记录已落盘: {p}")

    if n_fail:
        print(f"FAIL Phase {args.phase} 交接校验不通过，修正后再进入下一环节")
        return 1
    print(f"PASS Phase {args.phase} 交接校验通过（语义项仍需人工/sub agent 确认）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
