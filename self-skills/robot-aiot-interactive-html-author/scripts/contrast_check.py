#!/usr/bin/env python3
"""WCAG 对比度实算与色彩配对判定（premium-review-fix.md 动效审查三法·对比度实测法 + design-system-standards.md §1 配对规则条 4 / §2 条 2 + visual-style-presets.md §2 温度判定）。

用法:
  python3 contrast_check.py '#19222e' '#f6f7f8'            # 比值 + AA/AAA 判定
  python3 contrast_check.py FG BG --large                  # 大字档阈值（AA 3.0 / AAA 4.5）
  python3 contrast_check.py FG BG --level aaa              # 按 AAA 判 pass/fail
  python3 contrast_check.py --pair pairs.txt               # 批量: 每行 "fg bg [标签]"，注释行以 ; 或 // 开头
  python3 contrast_check.py --pair pairs.json              # 或 JSON [{"fg","bg","label"}]
  python3 contrast_check.py --on-primary '#ddae2d'         # 白/近黑配对推导
  python3 contrast_check.py --temperature '#e76f51' ['#f8f7f6']  # 暖/冷判定
  python3 contrast_check.py --lift '#f6f7f8' '#1f6feb' [--amount 0.08]  # surface 抬升一档

规则:
  - 相对亮度: sRGB 通道 gamma 校正 c<=0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4，
    L = 0.2126R + 0.7152G + 0.0722B；对比度 = (L1+0.05)/(L2+0.05)
  - 判定阈值: AA 正文 4.5 / 大字 3.0；AAA 正文 7.0 / 大字 4.5；
    对比模式退出码 0=达阈值 1=不达
  - on-primary 禁止硬编码 #fff/#000 顶替: 取白/近黑中与主色实算 ≥4.5:1 的那个；
    近黑默认 #0a0a0a，可用 --near-black 覆盖
  - 温度: H∈[345,90] 暖、H∈[180,300] 冷、其余为过渡扇区——给了 surface 时按底色
    偏暖灰（R>B）还是偏冷灰（B>R）判
  - surface 抬升: 向 primary 色调偏移 5%-11%（默认 8%），不加阴影
"""

import argparse
import json
import os
import re
import sys

HEX_RE = re.compile(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")


def normalize_hex(s: str) -> str:
    m = HEX_RE.fullmatch(s.strip())
    if not m:
        raise ValueError(f"非法 hex: {s}")
    v = m.group(1)
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return "#" + v.lower()


def hex_to_rgb01(h: str):
    n = int(h[1:], 16)
    return ((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255


def rgb_to_hex(r: float, g: float, b: float) -> str:
    def q(x):
        return format(max(0, min(255, int(x * 255 + 0.5))), "02x")

    return "#" + q(r) + q(g) + q(b)


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(h: str) -> float:
    r, g, b = hex_to_rgb01(h)
    return (
        0.2126 * srgb_to_linear(r)
        + 0.7152 * srgb_to_linear(g)
        + 0.0722 * srgb_to_linear(b)
    )


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = rel_luminance(fg), rel_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def rgb_to_hsl(h: str):
    r, g, b = hex_to_rgb01(h)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    hue = 0.0
    if d != 0:
        if mx == r:
            hue = ((g - b) / d) % 6
        elif mx == g:
            hue = (b - r) / d + 2
        else:
            hue = (r - g) / d + 4
        hue *= 60
        if hue < 0:
            hue += 360
    l = (mx + mn) / 2
    s = 0.0 if d == 0 else d / (1 - abs(2 * l - 1))
    return hue, s, l


def verdict(ratio: float, large: bool):
    aa = 3.0 if large else 4.5
    aaa = 4.5 if large else 7.0
    return (
        f"AA {'PASS' if ratio >= aa else 'FAIL'}(≥{aa})  "
        f"AAA {'PASS' if ratio >= aaa else 'FAIL'}(≥{aaa})"
    )


def check_pair(fg: str, bg: str, label: str, large: bool, level: str):
    ratio = contrast_ratio(fg, bg)
    threshold = (3.0 if large else 4.5) if level == "aa" else (4.5 if large else 7.0)
    ok = ratio >= threshold
    tag = "OK  " if ok else "FAIL"
    name = f" {label}" if label else ""
    print(f"[{tag}]{name} {fg} on {bg}: {ratio:.2f}:1  {verdict(ratio, large)}")
    return ok


def load_pairs(path: str):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if path.endswith(".json"):
        data = json.loads(content)
        return [(d["fg"], d["bg"], d.get("label", "")) for d in data]
    pairs = []
    for line in content.splitlines():
        line = line.strip()
        # 注释前缀是 ; 或 //（不能用 #，hex 色值以 # 开头）
        if not line or line.startswith(";") or line.startswith("//"):
            continue
        parts = line.split(None, 2)
        if len(parts) < 2:
            raise ValueError(f"pair 行格式 'fg bg [标签]': {line}")
        pairs.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("colors", nargs="*", help="FG BG 两个 hex")
    ap.add_argument("--large", action="store_true", help="大字档阈值")
    ap.add_argument("--level", choices=["aa", "aaa"], default="aa")
    ap.add_argument("--pair", default="", help="批量配对文件（txt 行或 json）")
    ap.add_argument("--on-primary", default="", metavar="PRIMARY")
    ap.add_argument("--near-black", default="#0a0a0a")
    ap.add_argument("--temperature", default="", metavar="PRIMARY")
    ap.add_argument("--lift", nargs=2, default=None, metavar=("SURFACE", "PRIMARY"))
    ap.add_argument("--amount", type=float, default=0.08)
    args = ap.parse_args()

    try:
        if args.on_primary:
            primary = normalize_hex(args.on_primary)
            white = "#ffffff"
            near_black = normalize_hex(args.near_black)
            rw = contrast_ratio(white, primary)
            rb = contrast_ratio(near_black, primary)
            print(f"白 {white}: {rw:.2f}:1   近黑 {near_black}: {rb:.2f}:1")
            cands = [(r, c) for r, c in ((rw, white), (rb, near_black)) if r >= 4.5]
            if not cands:
                print("FAIL 主色与白/近黑均不足 4.5:1，主色本身需调整")
                sys.exit(1)
            best = max(cands)
            print(f"on-primary = {best[1]}（{best[0]:.2f}:1）")
            sys.exit(0)

        if args.temperature:
            primary = normalize_hex(args.temperature)
            h, s, l = rgb_to_hsl(primary)
            if h >= 345 or h <= 90:
                res = "暖（H∈[345,90] 红/品红/橙/黄）"
            elif 180 <= h <= 300:
                res = "冷（H∈[180,300] 青/蓝/紫）"
            else:
                sector = "(90,180) 黄绿/绿" if h < 180 else "(300,345) 洋红/粉紫"
                res = f"过渡扇区{sector}"
                if len(args.colors) >= 1:
                    surface = normalize_hex(args.colors[0])
                    sr, sg, sb = hex_to_rgb01(surface)
                    res += "，按底色判: " + (
                        "暖灰→暖"
                        if sr > sb
                        else "冷灰→冷"
                        if sb > sr
                        else "中性灰→人工判"
                    )
                else:
                    res += "，需给 surface hex 按底色偏暖灰/冷灰判"
            print(f"{primary}: H={h:.0f}° S={s:.0%} L={l:.0%} → {res}")
            sys.exit(0)

        if args.lift:
            surface = normalize_hex(args.lift[0])
            primary = normalize_hex(args.lift[1])
            if not (0.05 <= args.amount <= 0.11):
                print(
                    f"FAIL --amount {args.amount} 超出 5%-11% 偏移区间", file=sys.stderr
                )
                sys.exit(1)
            sr, sg, sb = hex_to_rgb01(surface)
            pr, pg, pb = hex_to_rgb01(primary)
            t = args.amount
            mixed = rgb_to_hex(
                sr + t * (pr - sr), sg + t * (pg - sg), sb + t * (pb - sb)
            )
            print(f"surface 抬升一档: {surface} → {mixed}（向 {primary} 偏移 {t:.0%}）")
            sys.exit(0)

        if args.pair:
            if not os.path.exists(args.pair):
                print(f"FAIL 文件不存在: {args.pair}", file=sys.stderr)
                sys.exit(1)
            pairs = load_pairs(args.pair)
            if not pairs:
                print("FAIL pair 文件为空", file=sys.stderr)
                sys.exit(1)
            all_ok = True
            for fg, bg, label in pairs:
                all_ok &= check_pair(
                    normalize_hex(fg), normalize_hex(bg), label, args.large, args.level
                )
            print(
                f"--- 配对汇总: {len(pairs)} 组, {'全部达标' if all_ok else '存在不达标'} ---"
            )
            sys.exit(0 if all_ok else 1)

        if len(args.colors) == 2:
            fg, bg = normalize_hex(args.colors[0]), normalize_hex(args.colors[1])
            ok = check_pair(fg, bg, "", args.large, args.level)
            sys.exit(0 if ok else 1)

        ap.print_usage(sys.stderr)
        print(
            "FAIL 需要 FG BG 两个 hex，或 --pair/--on-primary/--temperature/--lift 之一",
            file=sys.stderr,
        )
        sys.exit(2)
    except ValueError as e:
        print(f"FAIL {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
