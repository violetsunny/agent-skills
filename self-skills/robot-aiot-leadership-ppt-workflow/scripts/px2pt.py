#!/usr/bin/env python3
"""画布换算：1920x1080px → 960x540pt 确定性换算。

契约来源: references/phase5-ppt-delivery.md:59-77（2:1 换算、EMU 画布常量）、
          :62（字号 0.5pt 取整）、:135（行距倍数化）、:141（圆角 adj 公式）。

用法:
  python3 px2pt.py 48 28 16            # 长度换算: pt = px/2, EMU = pt*12700
  python3 px2pt.py --font 48 28        # 字号换算: 结果按 0.5pt 取整
  python3 px2pt.py --line-height 1.5   # 行距倍数: CSS line-height → PPTX 百分比倍数
  python3 px2pt.py --adj 16 400 200    # 圆角: radius_px w_pt h_pt → adj=radius_pt/(min(w,h)/2)
  python3 px2pt.py --canvas            # 打印画布 EMU 常量 (12192000 x 6858000)
  python3 px2pt.py --json in.json      # 批量换算, JSON 进 JSON 出; "-" 读 stdin

JSON 输入 schema（各键均可选）:
  {"length_px": [48], "font_px": [48], "line_height": [1.5],
   "adj": [{"radius_px": 16, "w_pt": 400, "h_pt": 200}]}

继承甲方模板时本换算不适用（phase5:66,158），缩放比 = 模板宽 pt / HTML 画布宽 px。
adj 超出 0-0.5 合法范围（phase5:140）→ FAIL 退出码 1。
"""

import argparse
import json
import sys

EMU_PER_PT = 12700
CANVAS_EMU_W = 12192000  # 13.333in = 960pt (phase5:75)
CANVAS_EMU_H = 6858000  # 7.5in = 540pt (phase5:76)


def px2pt(px):
    return px / 2.0


def px2emu(px):
    return int(round(px2pt(px) * EMU_PER_PT))


def font_pt(px):
    """字号换算并按 0.5pt 取整（phase5:62）。"""
    return round(px2pt(px) * 2) / 2.0


def line_height_pct(multiplier):
    """CSS line-height 倍数 → PPTX 百分比倍数行距（phase5:135）。"""
    return round(multiplier * 100, 4)


def radius_adj(radius_px, w_pt, h_pt):
    """圆角 adj = radius_pt / (min(w_pt,h_pt)/2)（phase5:141）。"""
    radius_pt = px2pt(radius_px)
    short_half = min(w_pt, h_pt) / 2.0
    if short_half <= 0:
        raise ValueError("w_pt/h_pt 必须为正数")
    return radius_pt, round(radius_pt / short_half, 4)


def fmt_num(v):
    return f"{v:g}"


def run_json(payload):
    out = {}
    fails = []
    out["length"] = [
        {"px": px, "pt": px2pt(px), "emu": px2emu(px)}
        for px in payload.get("length_px", [])
    ]
    out["font"] = [{"px": px, "pt": font_pt(px)} for px in payload.get("font_px", [])]
    out["line_height"] = [
        {"css": m, "pptx_percent": line_height_pct(m)}
        for m in payload.get("line_height", [])
    ]
    out["adj"] = []
    for item in payload.get("adj", []):
        radius_pt, adj = radius_adj(item["radius_px"], item["w_pt"], item["h_pt"])
        if not (0 <= adj <= 0.5):
            fails.append(
                f"adj={adj} 超出 0-0.5 合法范围 (radius_px={item['radius_px']} "
                f"w_pt={item['w_pt']} h_pt={item['h_pt']})"
            )
        out["adj"].append(
            {
                "radius_px": item["radius_px"],
                "radius_pt": radius_pt,
                "adj": adj,
            }
        )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    for f in fails:
        print("FAIL", f, file=sys.stderr)
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(
        description="px→pt/EMU 换算（1920x1080px 画布 → 960x540pt，2:1）"
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--font", action="store_true", help="字号模式: 0.5pt 取整")
    mode.add_argument(
        "--line-height", action="store_true", help="行距模式: 倍数 → PPTX 百分比"
    )
    mode.add_argument(
        "--adj", action="store_true", help="圆角模式: 后接 radius_px w_pt h_pt"
    )
    mode.add_argument("--canvas", action="store_true", help="打印画布 EMU 常量")
    mode.add_argument("--json", metavar="FILE", help="批量换算 JSON 文件, - 读 stdin")
    ap.add_argument(
        "values", nargs="*", type=float, help="px 值（或 --adj 的三个参数）"
    )
    args = ap.parse_args()

    if args.canvas:
        print(f"canvas_emu: {CANVAS_EMU_W} x {CANVAS_EMU_H}")
        print(
            f"canvas_pt:  {CANVAS_EMU_W // EMU_PER_PT} x {CANVAS_EMU_H // EMU_PER_PT}"
        )
        print(f"emu_per_pt: {EMU_PER_PT}")
        return 0

    if args.json:
        raw = (
            sys.stdin.read()
            if args.json == "-"
            else open(args.json, encoding="utf-8").read()
        )
        return run_json(json.loads(raw))

    if args.adj:
        if len(args.values) != 3:
            ap.error("--adj 需要 3 个参数: radius_px w_pt h_pt")
        radius_pt, adj = radius_adj(*args.values)
        print(f"radius_pt: {fmt_num(radius_pt)}")
        print(f"adj: {adj}")
        if not (0 <= adj <= 0.5):
            print("FAIL adj 超出 0-0.5 合法范围（phase5:140）", file=sys.stderr)
            return 1
        return 0

    if not args.values:
        ap.error("缺少 px 值（或使用 --canvas/--json）")

    if args.line_height:
        for m in args.values:
            if m > 10:
                print(
                    f"WARN line-height={m:g} 疑似绝对值 px，契约要求按倍数换算（phase5:135）",
                    file=sys.stderr,
                )
            print(f"{m:g} -> {fmt_num(line_height_pct(m))}%")
        return 0

    for px in args.values:
        if args.font:
            print(f"{px:g}px -> {fmt_num(font_pt(px))}pt (font, 0.5pt 取整)")
        else:
            print(f"{px:g}px -> {fmt_num(px2pt(px))}pt = {px2emu(px)}EMU")
    return 0


if __name__ == "__main__":
    sys.exit(main())
