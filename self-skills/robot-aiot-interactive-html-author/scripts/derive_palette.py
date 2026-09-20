#!/usr/bin/env python3
"""单一主色 → HSL 五角色色板推导（visual-style-presets.md §4 单一主色推导三步法 derivePalette 的逐字 Python 移植）。

用法:
  python3 derive_palette.py '#1F6FEB'          # 输出 8 个 token（含五角色中性阶梯）
  python3 derive_palette.py '#1F6FEB' --json   # JSON 输出

规则（md 三步法）:
  - 五角色明度阶梯: L 97%→92%→82%→42%→14% 生成 surface / surface-muted /
    outline / text-secondary / text-primary，同 H，中性色带主色饱和度（≤14%）
  - 主色 S 封顶 72%；secondary 取 (H+150)°、tertiary 取 (H+210)° 分裂互补位
  - on-primary 不在推导内，按白/近黑实算配对（跑 contrast_check.py --on-primary）
  - 推导后自检①: text-primary 对 surface 对比度实算 ≥4.5:1，
    不足把 text 的 L 压到 0.10 重算（本脚本自动执行并标注）
  - 输入非法 hex → FAIL 退出码 1
"""

import argparse
import json
import math
import re
import sys


def normalize_hex(hexstr: str) -> str:
    h = hexstr.strip()
    m = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", h)
    if not m:
        raise ValueError(f"非法 hex: {hexstr}")
    v = m.group(1)
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return "#" + v.lower()


def hex_to_rgb01(hexstr: str):
    n = int(hexstr[1:], 16)
    return ((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255


def rgb_to_hsl(r: float, g: float, b: float):
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    h = 0.0
    if d != 0:
        if mx == r:
            h = ((g - b) / d) % 6
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h = int(math.floor(h * 60 + 0.5))  # JS Math.round 语义（.5 向 +∞）
        if h < 0:
            h += 360
    l = (mx + mn) / 2
    s = 0.0 if d == 0 else d / (1 - abs(2 * l - 1))
    return h, s, l


def to_hex(hh: float, ss: float, ll: float) -> str:
    a = ss * min(ll, 1 - ll)

    def f(k):
        x = (k + hh / 30) % 12
        v = ll - a * max(-1, min(x - 3, 9 - x, 1))
        # JS Math.round 语义（.5 向 +∞），不用 Python banker's rounding
        return format(int(math.floor(255 * v + 0.5)), "02x")

    return "#" + f(0) + f(8) + f(4)


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(hexstr: str) -> float:
    r, g, b = hex_to_rgb01(hexstr)
    return (
        0.2126 * srgb_to_linear(r)
        + 0.7152 * srgb_to_linear(g)
        + 0.0722 * srgb_to_linear(b)
    )


def contrast(fg: str, bg: str) -> float:
    l1, l2 = rel_luminance(fg), rel_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def derive_palette(hexstr: str):
    r, g, b = hex_to_rgb01(hexstr)
    h, s, l = rgb_to_hsl(r, g, b)
    s_base = min(s, 0.72)
    s_neutral = min(s_base, 0.14)
    return {
        "--primary-color": to_hex(h, s_base, l),
        "--surface-color": to_hex(h, min(s_neutral, 0.12), 0.97),
        "--surface-muted": to_hex(h, s_neutral, 0.92),
        "--outline-color": to_hex(h, s_neutral, 0.82),
        "--text-secondary": to_hex(h, min(s_base, 0.20), 0.42),
        "--text-primary": to_hex(h, min(s_base, 0.30), 0.14),
        "--secondary-color": to_hex((h + 150) % 360, s_base * 0.8, l),
        "--tertiary-color": to_hex((h + 210) % 360, s_base * 0.6, min(l + 0.15, 0.85)),
    }, (h, s_base, l, s_neutral)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("primary", help="主色 hex（#rgb 或 #rrggbb）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        primary = normalize_hex(args.primary)
    except ValueError as e:
        print(f"FAIL {e}", file=sys.stderr)
        sys.exit(1)

    tokens, (h, s_base, l, s_neutral) = derive_palette(primary)

    # 自检①: text-primary 对 surface 对比度 ≥4.5:1，不足把 text 的 L 压到 0.10 重算
    ratio = contrast(tokens["--text-primary"], tokens["--surface-color"])
    adjusted = False
    if ratio < 4.5:
        tokens["--text-primary"] = to_hex(h, min(s_base, 0.30), 0.10)
        ratio = contrast(tokens["--text-primary"], tokens["--surface-color"])
        adjusted = True

    if args.json:
        print(json.dumps(tokens, ensure_ascii=False, indent=2))
    else:
        for k, v in tokens.items():
            print(f"{k}: {v}")
    note = "（自检①触发：L 压到 0.10 重算）" if adjusted else ""
    print(
        f"# 自检①: text-primary vs surface 对比度 {ratio:.2f}:1 "
        f"{'PASS' if ratio >= 4.5 else 'WARN 仍不足 4.5，人工复核'}{note}",
        file=sys.stderr,
    )
    print(
        "# on-primary 不在推导内: 跑 contrast_check.py --on-primary "
        + tokens["--primary-color"],
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
