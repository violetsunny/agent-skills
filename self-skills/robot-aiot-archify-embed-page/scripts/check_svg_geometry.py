#!/usr/bin/env python3
"""内联 SVG 几何扫描：检测「后绘 rect 遮盖先绘 line/path」与「箭头尖端埋入后绘 rect」。

三类 finding：PARSE ERROR / arrow tip buried in later rect / line/path covered >=50% by later rect(s)。
path 支持 M/L/H/V/Q/C/Z（相对命令转大写），贝塞尔采样 24 点/段。
遮罩惯例：archify 产物用 fill=#f5f5f5 且 h<=24 的 rect 做标签遮罩，属通用产物惯例，默认豁免（可参数覆盖）。

用法:
  python3 check_svg_geometry.py <root> [--glob '*.html'] [--include-artifacts]
      [--mask-fill '#f5f5f5'] [--mask-max-h 24]
缺省扫 root 下 glob + index.html；--include-artifacts 追加 archify-*.html（窄 glob 时补 artifact 缺口）。
有 finding → exit 1。exit 0 不等于视觉通过，仍须与截图联合判定（references/rebuild-mode.md §6）。
check_file(Path) 可 import 单独调用（传 Path 对象，传 str 报 AttributeError）；仅 stdlib。
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def strip_ns(tag):
    return tag.split("}")[-1]


def path_segments(d):
    toks = re.findall(r"[MLHVQCZmlhvqcz]|-?\d*\.?\d+", d)
    segs = []
    cur = [0.0, 0.0]
    start = cur[:]
    cmd = None
    i = 0
    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t):
            cmd = t.upper()
            i += 1
            continue
        if cmd == "M":
            cur = [num(toks[i]), num(toks[i + 1])]
            start = cur[:]
            segs.append(("M", cur[:]))
            i += 2
            cmd = "L"
        elif cmd == "L":
            p1 = [num(toks[i]), num(toks[i + 1])]
            segs.append(("L", cur[:], p1))
            cur = p1
            i += 2
        elif cmd == "H":
            p1 = [num(toks[i]), cur[1]]
            segs.append(("L", cur[:], p1))
            cur = p1
            i += 1
        elif cmd == "V":
            p1 = [cur[0], num(toks[i])]
            segs.append(("L", cur[:], p1))
            cur = p1
            i += 1
        elif cmd == "Q":
            c = [num(toks[i]), num(toks[i + 1])]
            p1 = [num(toks[i + 2]), num(toks[i + 3])]
            segs.append(("Q", cur[:], c, p1))
            cur = p1
            i += 4
        elif cmd == "C":
            c1 = [num(toks[i]), num(toks[i + 1])]
            c2 = [num(toks[i + 2]), num(toks[i + 3])]
            p1 = [num(toks[i + 4]), num(toks[i + 5])]
            segs.append(("C", cur[:], c1, c2, p1))
            cur = p1
            i += 6
        elif cmd == "Z":
            segs.append(("L", cur[:], start[:]))
            cur = start[:]
            cmd = None
        else:
            i += 1
    return segs


def sample(segs, per=24):
    pts = []
    for s in segs:
        if s[0] == "M":
            pts.append(s[1])
        elif s[0] == "L":
            p0, p1 = s[1], s[2]
            for k in range(per + 1):
                t = k / per
                pts.append([p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t])
        elif s[0] == "Q":
            p0, c, p1 = s[1], s[2], s[3]
            for k in range(per + 1):
                t = k / per
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t**2 * p1[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t**2 * p1[1]
                pts.append([x, y])
        elif s[0] == "C":
            p0, c1, c2, p1 = s[1], s[2], s[3], s[4]
            for k in range(per + 1):
                t = k / per
                x = (
                    (1 - t) ** 3 * p0[0]
                    + 3 * (1 - t) ** 2 * t * c1[0]
                    + 3 * (1 - t) * t**2 * c2[0]
                    + t**3 * p1[0]
                )
                y = (
                    (1 - t) ** 3 * p0[1]
                    + 3 * (1 - t) ** 2 * t * c1[1]
                    + 3 * (1 - t) * t**2 * c2[1]
                    + t**3 * p1[1]
                )
                pts.append([x, y])
    return pts


def is_mask_rect(r, mask_fill="#f5f5f5", mask_max_h=24):
    return r["fill"] == mask_fill and r["h"] <= mask_max_h


def check_file(path, mask_fill="#f5f5f5", mask_max_h=24):
    html = path.read_text(encoding="utf-8")
    findings = []
    for m in re.finditer(r"<svg\b.*?</svg>", html, re.S):
        svg_xml = m.group(0)
        line_no = html[: m.start()].count("\n") + 1
        try:
            root = ET.fromstring(svg_xml)
        except ET.ParseError as e:
            findings.append((line_no, "PARSE ERROR", str(e)))
            continue
        title = ""
        elems = []
        for el in root.iter():
            tag = strip_ns(el.tag)
            if tag == "title":
                title = (el.text or "").strip()
            if tag in ("rect", "line", "path"):
                elems.append((tag, el))
        rects = []
        for idx, (tag, el) in enumerate(elems):
            if tag != "rect":
                continue
            w_s, h_s = el.get("width", ""), el.get("height", "")
            if "100%" in w_s or "100%" in h_s:
                continue
            r = {
                "idx": idx,
                "x": num(el.get("x")),
                "y": num(el.get("y")),
                "w": num(w_s),
                "h": num(h_s),
                "fill": (el.get("fill") or "").strip(),
            }
            rects.append(r)
        for idx, (tag, el) in enumerate(elems):
            if tag not in ("line", "path"):
                continue
            if el.get("marker-end") is None and el.get("stroke") is None:
                continue
            if tag == "line":
                segs = [
                    (
                        "L",
                        [num(el.get("x1")), num(el.get("y1"))],
                        [num(el.get("x2")), num(el.get("y2"))],
                    )
                ]
            else:
                segs = path_segments(el.get("d", ""))
            pts = sample(segs)
            if not pts:
                continue
            covered = 0
            coverers = set()
            for p in pts:
                for r in rects:
                    if r["idx"] <= idx:
                        continue
                    if r["fill"] in ("", "none"):
                        continue
                    if is_mask_rect(r, mask_fill, mask_max_h):
                        continue
                    if (
                        r["x"] < p[0] < r["x"] + r["w"]
                        and r["y"] < p[1] < r["y"] + r["h"]
                    ):
                        covered += 1
                        coverers.add((r["x"], r["y"], r["w"], r["h"], r["fill"]))
                        break
            frac = covered / len(pts)
            if el.get("marker-end") is not None and pts:
                tip = pts[-1]
                for r in rects:
                    if (
                        r["idx"] <= idx
                        or r["fill"] in ("", "none")
                        or is_mask_rect(r, mask_fill, mask_max_h)
                    ):
                        continue
                    if (
                        r["x"] < tip[0] < r["x"] + r["w"]
                        and r["y"] < tip[1] < r["y"] + r["h"]
                    ):
                        findings.append(
                            (
                                line_no,
                                title,
                                f"arrow tip ({tip[0]:.0f},{tip[1]:.0f}) buried in later rect ({r['x']:.0f},{r['y']:.0f},{r['w']:.0f},{r['h']:.0f})",
                            )
                        )
                        break
            if frac >= 0.5:
                desc = f"{tag} covered {frac:.0%} by later rect(s): {sorted(coverers)}"
                if tag == "line":
                    desc = (
                        f"line ({el.get('x1')},{el.get('y1')})-({el.get('x2')},{el.get('y2')}) "
                        + desc
                    )
                else:
                    desc = f'path d="{el.get("d")}" ' + desc
                findings.append((line_no, title, desc))
    return findings


def main():
    ap = argparse.ArgumentParser(description="内联 SVG 几何扫描（遮盖/箭头埋入）")
    ap.add_argument("root", help="扫描根目录")
    ap.add_argument("--glob", default="*.html", help="页面 glob（默认 *.html）")
    ap.add_argument(
        "--include-artifacts",
        action="store_true",
        help="追加 archify-*.html（窄 glob 时补 artifact 缺口）",
    )
    ap.add_argument(
        "--mask-fill", default="#f5f5f5", help="遮罩 rect fill（archify 惯例）"
    )
    ap.add_argument("--mask-max-h", type=float, default=24, help="遮罩 rect 最大高度")
    args = ap.parse_args()
    root = Path(args.root)
    files = sorted(set(root.glob(args.glob)))
    idx = root / "index.html"
    if idx.exists():
        files.append(idx)
    if args.include_artifacts:
        files += sorted(root.glob("archify-*.html"))
    total = 0
    for f in sorted(set(files)):
        if not f.exists():
            continue
        for line_no, title, desc in check_file(f, args.mask_fill, args.mask_max_h):
            total += 1
            print(f"{f.name}:{line_no} [{title}] {desc}")
    print(f"-- {total} finding(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
