#!/usr/bin/env python3
"""演示母稿静态 lint（标准库 re，零依赖）。

契约来源: robot-aiot-web-presentation-workflow/references/phase2-pagination.md
          （分页原则/节奏控制/主题节奏/能量段位/阻塞条件）、
          templates/deck-manuscript.md（章节顺序与表头解析契约）。

用法:
  python3 lint_manuscript.py <演示母稿.md>

检查（FAIL=阻塞，WARN=记录）:
  1. 每页四要素（标题/结论/上屏内容/话术）齐全且非空 → FAIL
  2. 图表需求节：缺节 → WARN；缺"类型"或类型非"无"却缺"名称" → FAIL；缺"配套素材图" → WARN
  3. 页数 >15 且头部无扩充口径 → FAIL；<5 → WARN
  4. 连续 3 页同页面类型（封面/尾页豁免） → FAIL
  5. 能量段位表缺失 → FAIL；四段位不齐（8 页以下允许缺铺垫谷）→ FAIL；
     全场无"高"能量（无峰）→ FAIL；末页落在铺垫谷 → FAIL
  6. 主题节奏表缺失 → WARN（仅登记版式 deck 强制）；表存在时：
     light/dark 两系混排 → FAIL（全 deck 单色系）；连续 3 页以上 hero → FAIL；
     8 页以上无 hero 档 → FAIL
  7. 疑似未替换模板占位符（<...> 尖括号占位） → WARN
  8. 头部元信息缺 汇报对象/结构形态 → WARN

退出码: 有 FAIL → 1，否则 0。
"""

import re
import sys

PAGE_RE = re.compile(r"^##\s*Page\s*(\d+)\s*[:：]\s*(.*)$")
SECTION_RE = re.compile(r"^##\s+(?!Page\b)(.+?)\s*$")
SUB_RE = re.compile(r"^###\s+(.+?)\s*$")
PLACEHOLDER_RE = re.compile(r"<[^<>\n]{0,60}>")
RHYTHM_SKIP_RE = re.compile(r"不使用登记版式")

FOUR_ELEMENTS = ["标题", "结论", "上屏内容", "话术"]
SEGMENTS = ["开场峰", "铺垫谷", "中段起伏", "收尾峰"]
THEMES = {"light", "dark", "hero light", "hero dark"}
RHYTHM_EXEMPT_TYPES = ("封面", "尾页", "致谢")


def parse_manuscript(text):
    lines = text.splitlines()
    header_quotes = []
    sections = {}  # 名称 -> 行列表
    pages = []  # {num, type, title, subs: {名: 行列表}, line}
    cur_section = None
    cur_page = None
    cur_sub = None
    for i, line in enumerate(lines, 1):
        m = PAGE_RE.match(line)
        if m:
            cur_page = {
                "num": int(m.group(1)),
                "raw_title": m.group(2),
                "subs": {},
                "line": i,
            }
            rest = m.group(2)
            for sep in ("—", "──", " - ", "–"):
                if sep in rest:
                    parts = rest.split(sep, 1)
                    cur_page["type"] = parts[0].strip()
                    cur_page["title"] = parts[1].strip()
                    break
            else:
                cur_page["type"] = rest.strip()
                cur_page["title"] = ""
            pages.append(cur_page)
            cur_section = None
            cur_sub = None
            continue
        m = SECTION_RE.match(line)
        if m:
            cur_section = m.group(1)
            sections.setdefault(cur_section, [])
            cur_page = None
            cur_sub = None
            continue
        if cur_page is not None:
            m = SUB_RE.match(line)
            if m:
                cur_sub = m.group(1)
                cur_page["subs"].setdefault(cur_sub, [])
                continue
            if cur_sub is not None:
                cur_page["subs"][cur_sub].append(line)
        elif cur_section is not None:
            sections[cur_section].append(line)
        elif line.startswith(">"):
            header_quotes.append(line)
    return header_quotes, sections, pages


def table_rows(lines):
    rows = []
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # 去表头


def body_of(sub_lines):
    out = []
    for line in sub_lines:
        s = line.strip()
        if s and not s.startswith("<!--"):
            out.append(s)
    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()

    fails, warns = [], []

    def fail(msg):
        fails.append(msg)

    def warn(msg):
        warns.append(msg)

    header, sections, pages = parse_manuscript(text)

    if not pages:
        print(
            "[MS-FAIL] 未解析到任何 '## Page N:' 页面块（检查是否用 templates/deck-manuscript.md 骨架）"
        )
        sys.exit(1)

    # 8. 头部元信息
    header_text = "\n".join(header)
    for field in ("汇报对象", "结构形态"):
        if field not in header_text:
            warn(f"头部元信息缺「{field}」")

    # 3. 页数
    n = len(pages)
    has_expand = "扩充口径" in header_text and not re.search(
        r"扩充口径[:：]\s*无", header_text
    )
    if n > 15 and not has_expand:
        fail(f"页面总数 {n} 超 15 页上限且头部无扩充口径记录")
    if n < 5:
        warn(f"页面总数 {n} 少于 5 页，检查是否遗漏关键信息")

    # 1/2. 逐页四要素与图表需求
    for p in pages:
        tag = f"Page {p['num']}(:{p['line']})"
        for el in FOUR_ELEMENTS:
            matched = [k for k in p["subs"] if k.startswith(el)]
            if not matched:
                fail(f"{tag} 缺四要素「{el}」节")
            elif not body_of(p["subs"][matched[0]]):
                fail(f"{tag} 四要素「{el}」为空")
            elif el == "上屏内容" and len(body_of(p["subs"][matched[0]])) < 2:
                warn(f"{tag} 上屏内容不足 2 行，疑似标题级骨架")
        chart_keys = [k for k in p["subs"] if k.startswith("图表需求")]
        if not chart_keys:
            warn(f"{tag} 缺「图表需求」节（不需要图表也应保留节并写 类型：无）")
        else:
            body = "\n".join(body_of(p["subs"][chart_keys[0]]))
            m = re.search(r"类型[:：]\s*(\S+)", body)
            if not m:
                fail(f"{tag} 图表需求缺「类型」标注")
            elif m.group(1) != "无" and not re.search(r"名称[:：]\s*\S+", body):
                fail(f"{tag} 图表类型为「{m.group(1)}」但缺「名称」")
            if "配套素材图" not in body:
                warn(f"{tag} 图表需求缺「配套素材图」标注（无素材应显式写 无）")

    # 4. 连续同类型
    run_type, run_start, run_len = None, None, 0
    for p in pages:
        exempt = any(t in p["type"] for t in RHYTHM_EXEMPT_TYPES)
        if exempt:
            run_type, run_len = None, 0
            continue
        if p["type"] == run_type:
            run_len += 1
            if run_len >= 3:
                fail(
                    f"Page {run_start}-{p['num']} 连续 {run_len} 页同类型「{run_type}」，须插过渡页或换版式"
                )
        else:
            run_type, run_start, run_len = p["type"], p["num"], 1

    # 5. 能量段位表
    seg_section = [k for k in sections if "能量段位" in k]
    if not seg_section:
        fail("缺「能量段位表」章节（母稿阶段必须规划能量骨架）")
    else:
        rows = table_rows(sections[seg_section[0]])
        if not rows:
            fail("「能量段位表」无数据行")
        else:
            segs = [r[1] for r in rows if len(r) >= 3]
            levels = [r[2] for r in rows if len(r) >= 3]
            missing = [s for s in SEGMENTS if not any(s in x for x in segs)]
            if n >= 8:
                for s in missing:
                    fail(f"能量段位表缺「{s}」段位（8 页以上四段位必须齐全）")
            else:
                for s in missing:
                    if s != "铺垫谷":
                        fail(f"能量段位表缺「{s}」段位（开场峰/收尾峰不可省）")
            if not any("高" in x for x in levels):
                fail("能量段位表全场无「高」能量页（无峰 = 无记忆点）")
            if segs and "铺垫谷" in segs[-1]:
                fail("铺垫谷落在末页（铺垫谷不得落尾部）")

    # 6. 主题节奏表
    rhythm_section = [k for k in sections if "主题节奏" in k]
    if not rhythm_section:
        warn(
            "缺「主题节奏表」章节（登记版式 S/M 系 deck 为阻塞项，请人工确认版式归属）"
        )
    else:
        rlines = sections[rhythm_section[0]]
        if any(RHYTHM_SKIP_RE.search(x) for x in rlines):
            pass  # 显式声明不使用登记版式
        else:
            rows = [r for r in table_rows(rlines) if len(r) >= 2]
            if not rows:
                warn("「主题节奏表」无数据行")
            else:
                themes = [r[1].lower() for r in rows]
                unknown = [t for t in themes if t not in THEMES]
                if unknown:
                    warn(
                        f"主题档存在枚举外取值: {sorted(set(unknown))}（合法: light/dark/hero light/hero dark）"
                    )
                families = {t.split()[-1] for t in themes if t in THEMES}
                if len(families) > 1:
                    fail(
                        f"主题节奏表混排 light/dark 两系 {sorted(families)}（全 deck 单色系：全 light 系或全 dark 系，禁止交替）"
                    )
                run_hero, run_start_idx, run_l = None, 0, 0
                for idx, t in enumerate(themes):
                    hero = t.startswith("hero")
                    if run_hero is hero:
                        run_l += 1
                    else:
                        if run_hero is True and run_l >= 3:
                            fail(
                                f"主题节奏表第 {run_start_idx + 1}-{run_start_idx + run_l} 行连续 {run_l} 页 hero（不超过 2 页）"
                            )
                        run_hero, run_start_idx, run_l = hero, idx, 1
                if run_hero is True and run_l >= 3:
                    fail(
                        f"主题节奏表第 {run_start_idx + 1}-{run_start_idx + run_l} 行连续 {run_l} 页 hero（不超过 2 页）"
                    )
                if n >= 8 and not any(t.startswith("hero") for t in themes):
                    fail("8 页以上 deck 主题节奏表无 hero 档（章节交界呼吸点缺失）")

    # 7. 占位符
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("<!--"):
            continue
        for m in PLACEHOLDER_RE.finditer(line):
            s = m.group(0)
            if "..." in s or re.search(r"<(chart-name|YYYY|项目|页面|受众|简短)", s):
                warn(f":{i} 疑似未替换模板占位符 {s}")

    for w in warns:
        print(f"[MS-WARN] {w}")
    for f_ in fails:
        print(f"[MS-FAIL] {f_}")
    print(f"[MS-SUMMARY] pages={n} fail={len(fails)} warn={len(warns)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
