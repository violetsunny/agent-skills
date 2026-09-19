#!/usr/bin/env python3
"""演讲时间预算断言（presenter-mode §16 条 8）：静态扫 SPEAKER_NOTES 的 minutes 字段。

用法:
  python3 minutes_budget.py <deck.html 或 pages 目录> --target 20
规则:
  - 全部页都声明 minutes 时才求和断言
  - 总计划 > 目标 × 90%  → FAIL（超时，须留 10% 现场缓冲）
  - 总计划 < 目标 × 55%  → WARN（脚本量不足）
  - 部分页缺 minutes     → 跳过求和，明示 "timing is partial"，禁止局部凑总数
"""

import argparse
import os
import re
import sys

MINUTES_RE = re.compile(r"\bminutes\s*:\s*(\d+(?:\.\d+)?)")
SLIDEID_RE = re.compile(r"\bslideId\s*:")
SECTION_RE = re.compile(r"<section\b[^>]*class\s*=\s*\"[^\"]*\bslide\b", re.I)


def scan(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    minutes = [float(m) for m in MINUTES_RE.findall(src)]
    pages = len(SLIDEID_RE.findall(src)) or len(SECTION_RE.findall(src))
    return minutes, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument(
        "--target-minutes", "--target", dest="target", type=float, required=True
    )
    args = ap.parse_args()

    files = []
    if os.path.isdir(args.deck):
        files = sorted(
            os.path.join(args.deck, f)
            for f in os.listdir(args.deck)
            if f.endswith(".html")
        )
    else:
        files = [args.deck]

    all_minutes, all_pages = [], 0
    for f in files:
        m, p = scan(f)
        all_minutes += m
        all_pages += p
        print(f"{os.path.basename(f)}: pages={p} minutes条目={len(m)} 值={m}")

    if not all_minutes:
        print("timing is partial: 无页声明 minutes，跳过求和断言")
        sys.exit(0)
    if all_pages and len(all_minutes) < all_pages:
        print(
            f"timing is partial: {len(all_minutes)}/{all_pages} 页声明 minutes，跳过求和断言"
        )
        sys.exit(0)
    if not all_pages:
        print(
            f"页数探测失败（无 slideId 也无 section.slide），按 minutes 条目数 {len(all_minutes)} 求和"
        )

    total = sum(all_minutes)
    print(f"总计划 {total:g} 分钟 / 目标 {args.target:g} 分钟")
    if total > args.target * 0.9:
        print(f"FAIL 总计划超过目标×90%（{args.target * 0.9:g}），超时风险，压缩脚本")
        sys.exit(1)
    if total < args.target * 0.55:
        print(f"WARN 总计划低于目标×55%（{args.target * 0.55:g}），脚本量不足")
    print("PASS 时间预算在区间内")


if __name__ == "__main__":
    main()
