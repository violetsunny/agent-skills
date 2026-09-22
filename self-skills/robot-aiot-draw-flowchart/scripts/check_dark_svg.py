#!/usr/bin/env python3
"""Dark-theme SVG pre-delivery checks.

Contract source: references/dark-svg-techniques.md
  - §2.1 硬约束 (lines 74-79): 7px font floor; body-text contrast >= 4.5:1;
    large text (>=18px) and graphic elements >= 3:1; #475569 and darker slate
    forbidden for body text; secondary text unified at #94a3b8.
  - §2.2 连线与降权: connector strokes >= #64748b (checked as >=3:1 graphic contrast).
  - §7/§8 viewBox rule: viewBox = content bbox + 30px padding on all sides.
  - §8 item 6: CJK labels need a CJK-capable font-family fallback
    ('Noto Sans SC','PingFang SC' etc.).
  - §9 交付前自检 (lines 287-294).

Standard library only. Usage:
    python3 check_dark_svg.py <file.svg> [--bg HEX]

--bg overrides background auto-detection (the first rect covering >=90% of the
viewBox; fallback #0f172a). Exit 0 = no errors (warnings allowed), 1 = errors.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)")
SLATE_DARK_FOR_TEXT = {"#475569", "#334155", "#1e293b", "#0f172a", "#020617"}
CJK_FAMILIES = (
    "noto sans sc",
    "pingfang sc",
    "microsoft yahei",
    "hiragino sans gb",
    "source han sans",
    "wenquanyi",
    "simhei",
    "simsun",
    "stheiti",
    "microsoft jhenghei",
)
NAMED_COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#ff0000",
    "gray": "#808080",
    "grey": "#808080",
    "silver": "#c0c0c0",
    "navy": "#000080",
    "teal": "#008080",
    "orange": "#ffa500",
    "cyan": "#00ffff",
    "gold": "#ffd700",
}
MIN_FONT_PX = 7.0
BODY_CONTRAST = 4.5
LARGE_CONTRAST = 3.0
LARGE_FONT_PX = 18.0
VIEWBOX_PADDING = 30.0
PADDING_TOLERANCE = 2.0  # stroke overshoot allowance
EXCLUDED_ROLES = {"background", "bridge-mask", "decoration", "legend"}


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def parse_color(value: str | None) -> tuple[float, float, float, float] | None:
    """Return (r, g, b, a) in 0-255/0-1, or None if unresolvable."""
    if not value:
        return None
    value = value.strip()
    if value.lower() in ("none", "transparent", "currentcolor", "inherit", "url"):
        return None
    if value.lower() in NAMED_COLORS:
        value = NAMED_COLORS[value.lower()]
    m = re.match(r"^#([0-9a-fA-F]{3})$", value)
    if m:
        r, g, b = (int(c * 2, 16) for c in m.group(1))
        return (r, g, b, 1.0)
    m = re.match(r"^#([0-9a-fA-F]{6})$", value)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.match(r"^rgba?\(\s*([^)]+)\s*\)$", value)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        try:
            r, g, b = (float(p) for p in parts[:3])
            a = float(parts[3]) if len(parts) > 3 else 1.0
            return (r, g, b, a)
        except ValueError:
            return None
    return None


def to_hex(rgb: tuple[float, float, float, float]) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def composite(
    fg: tuple[float, float, float, float], bg: tuple[float, float, float, float]
):
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def relative_luminance(rgb) -> float:
    def channel(c: float) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg) -> float:
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


@dataclass
class Affine:
    """Scale + translate only (rotation/skew ignored, documented limitation)."""

    a: float = 1.0
    d: float = 1.0
    e: float = 0.0
    f: float = 0.0

    def compose(self, other: "Affine") -> "Affine":
        return Affine(
            self.a * other.a,
            self.d * other.d,
            self.a * other.e + self.e,
            self.d * other.f + self.f,
        )

    def apply(self, x: float, y: float) -> tuple[float, float]:
        return (self.a * x + self.e, self.d * y + self.f)

    @property
    def scale(self) -> float:
        return min(abs(self.a), abs(self.d))


def parse_transform(value: str | None) -> Affine:
    if not value:
        return Affine()
    result = Affine()
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", value):
        nums = [float(n) for n in NUMBER_RE.findall(args)]
        if name == "translate" and nums:
            result = result.compose(
                Affine(e=nums[0], f=nums[1] if len(nums) > 1 else 0.0)
            )
        elif name == "scale" and nums:
            sx = nums[0]
            sy = nums[1] if len(nums) > 1 else sx
            result = result.compose(Affine(a=sx, d=sy))
        elif name == "matrix" and len(nums) == 6:
            result = result.compose(Affine(a=nums[0], d=nums[3], e=nums[4], f=nums[5]))
    return result


def collect_css(root: ET.Element) -> dict[str, dict[str, str]]:
    """selector -> {prop: value}; selectors kept raw ('text', '.foo', '*')."""
    rules: dict[str, dict[str, str]] = {}
    for style in root.iter():
        if local_name(style.tag) != "style" or not style.text:
            continue
        text = re.sub(
            r"@[^{]*\{[^}]*\}", "", style.text
        )  # drop @import/@font-face blocks
        for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", text):
            for sel in selector.split(","):
                sel = sel.strip()
                if not sel:
                    continue
                props = rules.setdefault(sel, {})
                for decl in body.split(";"):
                    if ":" in decl:
                        k, v = decl.split(":", 1)
                        props[k.strip().lower()] = (
                            v.strip().rstrip("!important").strip()
                        )
    return rules


def css_lookup(el: ET.Element, prop: str, css: dict[str, dict[str, str]]) -> str | None:
    for cls in (el.get("class") or "").split():
        if f".{cls}" in css and prop in css[f".{cls}"]:
            return css[f".{cls}"][prop]
    tag = local_name(el.tag)
    if tag in css and prop in css[tag]:
        return css[tag][prop]
    if "*" in css and prop in css["*"]:
        return css["*"][prop]
    return None


def inline_style(el: ET.Element, prop: str) -> str | None:
    style = el.get("style")
    if not style:
        return None
    for decl in style.split(";"):
        if ":" in decl:
            k, v = decl.split(":", 1)
            if k.strip().lower() == prop:
                return v.strip()
    return None


def effective(
    el: ET.Element, prop: str, css: dict, inherited: str | None
) -> str | None:
    for value in (
        inline_style(el, prop),
        css_lookup(el, prop, css),
        el.get(prop),
        inherited,
    ):
        if value:
            return value
    return None


def has_cjk(text: str) -> bool:
    return any(
        0x4E00 <= ord(c) <= 0x9FFF
        or 0x3400 <= ord(c) <= 0x4DBF
        or 0x3000 <= ord(c) <= 0x303F
        or 0xFF00 <= ord(c) <= 0xFFEF
        for c in text
    )


def text_content(el: ET.Element) -> str:
    return "".join(el.itertext()).strip()


def font_family_has_cjk(family: str | None) -> bool:
    if not family:
        return False
    lowered = family.lower()
    return any(name in lowered for name in CJK_FAMILIES)


def viewBox_of(root: ET.Element) -> tuple[float, float, float, float] | None:
    nums = [float(n) for n in NUMBER_RE.findall(root.get("viewBox", ""))]
    if len(nums) != 4:
        return None
    return tuple(nums)  # type: ignore[return-value]


def is_canvas_rect(el: ET.Element, vb: tuple[float, float, float, float]) -> bool:
    try:
        w = float(el.get("width", "0"))
        h = float(el.get("height", "0"))
    except ValueError:
        return False
    area = vb[2] * vb[3]
    return area > 0 and w * h >= 0.9 * area


def detect_background(root: ET.Element, vb: tuple[float, float, float, float]):
    area = vb[2] * vb[3]
    for el in root.iter():
        if local_name(el.tag) != "rect":
            continue
        try:
            w = float(el.get("width", "0"))
            h = float(el.get("height", "0"))
        except ValueError:
            continue
        if area > 0 and w * h >= 0.9 * area:
            color = parse_color(el.get("fill"))
            if color:
                return color, f"auto-detected background rect fill {to_hex(color)}"
    return (15.0, 23.0, 42.0, 1.0), "no background rect found; assuming #0f172a"


@dataclass
class WalkState:
    affine: Affine
    role: str | None
    fill: str | None
    stroke: str | None
    font_size: str | None
    font_family: str | None
    in_defs: bool


def walk(root: ET.Element):
    stack = [(root, WalkState(Affine(), None, None, None, None, None, False))]
    while stack:
        el, st = stack.pop()
        yield el, st
        tag = local_name(el.tag)
        role = (el.get("data-graph-role") or st.role or "").strip().lower() or None
        child = WalkState(
            st.affine.compose(parse_transform(el.get("transform"))),
            role if role in EXCLUDED_ROLES or role in ("node", "label") else st.role,
            effective(el, "fill", {}, st.fill) if tag != "text" else st.fill,
            effective(el, "stroke", {}, st.stroke),
            effective(el, "font-size", {}, st.font_size),
            effective(el, "font-family", {}, st.font_family),
            st.in_defs or tag in ("defs", "pattern", "marker", "symbol"),
        )
        for c in reversed(list(el)):
            stack.append((c, child))


def shape_points(el: ET.Element) -> list[tuple[float, float]]:
    tag = local_name(el.tag)

    def num(name: str, default: float = 0.0) -> float:
        try:
            return float(el.get(name, default))
        except ValueError:
            return default

    if tag == "rect":
        x, y, w, h = num("x"), num("y"), num("width"), num("height")
        return [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    if tag == "circle":
        cx, cy, r = num("cx"), num("cy"), num("r")
        return [(cx - r, cy - r), (cx + r, cy + r)]
    if tag == "ellipse":
        cx, cy, rx, ry = num("cx"), num("cy"), num("rx"), num("ry")
        return [(cx - rx, cy - ry), (cx + rx, cy + ry)]
    if tag in ("line",):
        return [(num("x1"), num("y1")), (num("x2"), num("y2"))]
    if tag in ("polyline", "polygon"):
        nums = [float(n) for n in NUMBER_RE.findall(el.get("points", ""))]
        return list(zip(nums[0::2], nums[1::2], strict=False))
    if tag == "path":
        nums = [
            float(n)
            for n in re.findall(
                r"[-+]?(?:\d*\.\d+|\d+\.?)", re.sub(r"[a-zA-Z]", " ", el.get("d", ""))
            )
        ]
        return list(zip(nums[0::2], nums[1::2], strict=False))
    return []


def estimate_text_bbox(el: ET.Element, font_size: float, affine: Affine):
    content = text_content(el)
    if not content:
        return None
    try:
        x = float(el.get("x", "0"))
        y = float(el.get("y", "0"))
    except ValueError:
        return None
    width = sum(font_size * (1.0 if has_cjk(c) else 0.55) for c in content)
    anchor = (el.get("text-anchor") or "start").strip()
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    top, bottom = y - font_size * 0.8, y + font_size * 0.25
    corners = [(x, top), (x + width, top), (x, bottom), (x + width, bottom)]
    return [affine.apply(*p) for p in corners]


def run_checks(
    path: Path, bg_override: str | None
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"cannot parse {path}: {exc}"], warnings, notes
    if local_name(root.tag) != "svg":
        return (
            [f"root element is <{local_name(root.tag)}>, expected <svg>"],
            warnings,
            notes,
        )

    vb = viewBox_of(root)
    if vb is None:
        errors.append("missing or malformed viewBox — cannot check padding")
        vb = (0.0, 0.0, 0.0, 0.0)

    css = collect_css(root)
    if bg_override:
        bg = parse_color(bg_override)
        if bg is None:
            errors.append(f"--bg value unparseable: {bg_override}")
            bg = (15.0, 23.0, 42.0, 1.0)
        bg_note = f"background from --bg {to_hex(bg)}"
    else:
        bg, bg_note = detect_background(root, vb)
    notes.append(bg_note)
    if relative_luminance(bg) > 0.2:
        # 弃权：浅色背景下深色规则不适用，继续套用只会产生误报。
        notes.append(
            f"background {to_hex(bg)} is light — 浅色背景，深色规则不适用，本检查弃权（exit 0）"
        )
        return [], [], notes

    content_pts: list[tuple[float, float]] = []
    text_count = 0

    for el, st in walk(root):
        tag = local_name(el.tag)
        if st.in_defs or tag in ("style", "script", "metadata", "title", "desc"):
            continue
        role = (el.get("data-graph-role") or st.role or "").strip().lower()
        own = st.affine.compose(parse_transform(el.get("transform")))

        if tag == "text":
            content = text_content(el)
            if not content:
                continue
            text_count += 1
            fs_str = effective(el, "font-size", css, st.font_size) or "16"
            try:
                fs = float(NUMBER_RE.match(fs_str.strip()).group(0))
            except (AttributeError, ValueError):
                fs = 16.0
                warnings.append(
                    f"text {content[:20]!r}: unparseable font-size {fs_str!r}; assuming 16"
                )
            eff_fs = fs * own.scale

            if eff_fs < MIN_FONT_PX - 1e-9:
                errors.append(
                    f"text {content[:24]!r}: effective font-size {eff_fs:.1f}px < {MIN_FONT_PX:.0f}px floor"
                )

            fill_str = effective(el, "fill", css, st.fill)
            color = parse_color(fill_str) if fill_str else None
            if fill_str is None:
                color = (0.0, 0.0, 0.0, 1.0)  # SVG initial fill is black
            if color is None:
                warnings.append(
                    f"text {content[:24]!r}: fill {fill_str!r} unresolvable; contrast skipped"
                )
            else:
                if color[3] < 1.0:
                    color = composite(color, bg)
                hexv = to_hex(color)
                if hexv in SLATE_DARK_FOR_TEXT:
                    errors.append(
                        f"text {content[:24]!r}: {hexv} (#475569 or darker slate) forbidden for body text"
                    )
                ratio = contrast_ratio(color, bg)
                need = LARGE_CONTRAST if eff_fs >= LARGE_FONT_PX else BODY_CONTRAST
                if ratio < need:
                    errors.append(
                        f"text {content[:24]!r}: contrast {ratio:.2f}:1 < {need:.1f}:1 "
                        f"({hexv} on {to_hex(bg)}, font-size {eff_fs:.1f}px)"
                    )

            if has_cjk(content):
                family = effective(el, "font-family", css, st.font_family)
                if not font_family_has_cjk(family):
                    errors.append(
                        f"text {content[:24]!r}: CJK content without CJK font-family fallback "
                        f"(need 'Noto Sans SC','PingFang SC' or similar; got {family!r})"
                    )

            bbox = estimate_text_bbox(el, fs, own)
            if bbox:
                content_pts.extend(bbox)
            continue

        # graphic elements: stroke contrast (>= 3:1), skip decoration/background roles
        if role not in EXCLUDED_ROLES:
            stroke_str = effective(el, "stroke", css, st.stroke)
            stroke = parse_color(stroke_str) if stroke_str else None
            if stroke:
                opaque = composite(stroke, bg) if stroke[3] < 1.0 else stroke
                ratio = contrast_ratio(opaque, bg)
                if ratio < LARGE_CONTRAST:
                    warnings.append(
                        f"<{tag} id={el.get('id', '-')!r}>: stroke {to_hex(opaque)} contrast "
                        f"{ratio:.2f}:1 < {LARGE_CONTRAST:.1f}:1 (graphic element minimum)"
                    )

        pts = shape_points(el)
        skip_bbox = role in ("label", "bridge-mask", "background") or (
            tag == "rect" and is_canvas_rect(el, vb)
        )
        if pts and not skip_bbox:
            content_pts.extend(own.apply(x, y) for x, y in pts)

    # viewBox padding
    if vb[2] > 0 and vb[3] > 0 and content_pts:
        xs = [p[0] for p in content_pts]
        ys = [p[1] for p in content_pts]
        margins = {
            "left": min(xs) - vb[0],
            "top": min(ys) - vb[1],
            "right": vb[0] + vb[2] - max(xs),
            "bottom": vb[1] + vb[3] - max(ys),
        }
        for side, margin in margins.items():
            if margin < 0:
                errors.append(
                    f"viewBox padding: content overflows {side} edge by {-margin:.1f}px"
                )
            elif margin < VIEWBOX_PADDING - PADDING_TOLERANCE:
                errors.append(
                    f"viewBox padding: {side} margin {margin:.1f}px < {VIEWBOX_PADDING:.0f}px "
                    f"(content bbox + 30px required; text widths are estimates)"
                )
            elif margin > VIEWBOX_PADDING * 2:
                warnings.append(
                    f"viewBox padding: {side} margin {margin:.1f}px > {VIEWBOX_PADDING * 2:.0f}px (excessive)"
                )
    elif vb[2] > 0 and not content_pts:
        warnings.append("no measurable content found; viewBox padding not checked")

    if text_count == 0:
        warnings.append(
            "no <text> elements found — font/contrast/CJK checks had nothing to inspect"
        )
    return errors, warnings, notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dark-theme SVG checks: WCAG contrast, 7px font floor, viewBox padding, CJK fallback."
    )
    parser.add_argument("svg_file", type=Path)
    parser.add_argument("--bg", help="background hex override (e.g. #0f172a)")
    args = parser.parse_args()

    errors, warnings, notes = run_checks(args.svg_file, args.bg)
    for item in notes:
        print(f"NOTE  {item}")
    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
