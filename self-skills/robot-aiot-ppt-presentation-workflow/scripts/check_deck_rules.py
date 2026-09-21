#!/usr/bin/env python3
"""Deck 级硬规则校验：布局序列 + 页数 + 时长。

契约来源: references/slide-layout-strategies.md:53-57（Deck 级硬规则 1-3）。

用法:
  python3 check_deck_rules.py "Title,Problem,Solution,Title" [--minutes 30]
  python3 check_deck_rules.py layouts.txt --minutes 45      # 文件每行一个布局名

规则:
  1. 相邻两页不得使用相同布局模式                          → FAIL (:55)
  2. 同一布局整套复用时至少间隔 2 页（两次出现索引差 >= 3） → FAIL (:55)
  3. 页数 >= 10 时目录页与章节过渡页必配                    → FAIL (:56)
  4. 时长↔页数换算表（md 原文表）: 30min=8-12, 45min=12-16, 60min=16-22 → FAIL (:57)

假设（md 未明确，按契约精神决定）:
  - 目录页识别: 布局名含 目录/toc/agenda/contents（不区分大小写）
  - 过渡页识别: 布局名含 过渡/章节/transition/section/divider
  - 时长不在换算表三档内时输出 WARN 不判定（表以 md 原文为准，不外推）
  - 布局名不做 17 种枚举校验（母稿可用自定义名，规则只约束序列关系）
"""

import argparse
import os
import sys

MINUTES_TABLE = {
    30: (8, 12),
    45: (12, 16),
    60: (16, 22),
}  # slide-layout-strategies.md:57
TOC_KEYWORDS = ("目录", "toc", "agenda", "contents")
TRANSITION_KEYWORDS = ("过渡", "章节", "transition", "section", "divider")


def match_any(name, keywords):
    low = name.lower()
    return any(k in low for k in keywords)


def main():
    ap = argparse.ArgumentParser(description="Deck 级硬规则校验")
    ap.add_argument("layouts", help="逗号分隔布局名序列，或每行一个布局名的文件路径")
    ap.add_argument("--minutes", type=int, default=None, help="演讲时长（分钟）")
    args = ap.parse_args()

    if os.path.isfile(args.layouts):
        with open(args.layouts, encoding="utf-8") as f:
            layouts = [line.strip() for line in f if line.strip()]
    else:
        layouts = [s.strip() for s in args.layouts.split(",") if s.strip()]

    if not layouts:
        print("FAIL 布局序列为空", file=sys.stderr)
        return 2

    n = len(layouts)
    fails = []
    print(f"页数: {n}")
    for i, name in enumerate(layouts, 1):
        print(f"  页{i}: {name}")

    # 规则 1: 相邻两页布局不同
    for i in range(1, n):
        if layouts[i] == layouts[i - 1]:
            fails.append(f"规则1 页{i}/页{i + 1} 相邻使用相同布局 '{layouts[i]}'")

    # 规则 2: 同一布局至少间隔 2 页
    seen = {}
    for i, name in enumerate(layouts):
        if name in seen and i - seen[name] < 3:
            fails.append(
                f"规则2 布局 '{name}' 页{seen[name] + 1} 与页{i + 1} 间隔不足 2 页"
            )
        seen[name] = i

    # 规则 3: 页数 >= 10 必配目录页与章节过渡页
    if n >= 10:
        if not any(match_any(x, TOC_KEYWORDS) for x in layouts):
            fails.append("规则3 页数 >= 10 但缺目录页")
        if not any(match_any(x, TRANSITION_KEYWORDS) for x in layouts):
            fails.append("规则3 页数 >= 10 但缺章节过渡页")

    # 规则 4: 时长↔页数换算表
    if args.minutes is not None:
        rng = MINUTES_TABLE.get(args.minutes)
        if rng is None:
            print(
                f"[WARN] 规则4 时长 {args.minutes}min 不在换算表 (30/45/60)，无法判定"
            )
        elif not (rng[0] <= n <= rng[1]):
            fails.append(
                f"规则4 时长 {args.minutes}min 应对应 {rng[0]}-{rng[1]} 页，实际 {n} 页"
            )

    if fails:
        print("FAIL Deck 级硬规则不通过:")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS Deck 级硬规则全过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
