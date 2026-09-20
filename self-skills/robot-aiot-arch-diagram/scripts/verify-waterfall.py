#!/usr/bin/env python3
"""Gate for the Waterfall Chart type.

Contract source: references/type-waterfall.md (layout conventions, element
pattern, anti-patterns, honesty rules): "scripts/verify-waterfall.py reads
each bar's declaration, recomputes the running totals, refits the shared
scale from the start anchor, and fails on any conservation, geometry, carry,
label, or sign-treatment drift." Domain rule per the same file: "the same
rule, cases, and all-zero fallback as the dumbbell (type-bar.md § Dumbbell
honesty rules)".

Checks implemented:
- declarations: every bar rect carries data-role in {total, delta, subtotal},
  a parsable data-value (totals/subtotals unsigned, deltas explicitly signed
  +/-), and a non-empty data-name
- walk structure: 3-8 bars, exactly two totals (start + end), at most one
  subtotal, bars strictly left to right in document order, first and last bar
  are totals, degenerate start (zero or negative total) is a named failure
- conservation: start + every signed bridge = each subtotal and the end
  total, exactly; zero bridges are dropped, never drawn
- shared scale: fitted from the tick labels (>= 2 distinct numeric ticks, all
  on one line, y decreasing as values grow); with fewer than two ticks the
  scale is refit from the start anchor (floor = 0, k from the start bar's
  drawn top) when that is sound, else the gate fails closed
- domain: the four dumbbell sign cases over the running levels, including the
  all-zero fallback span and the zero line at its scaled position in the
  axis-line weight when lo < 0 < hi
- geometry: totals/subtotals drawn from the baseline (y=420) to their level,
  bridges spanning exactly their two running levels (+/- 0.75px), endpoint
  positions rounded to integer pixels, bar x/width on the 4px grid, equal
  widths on an even pitch with bar >= 50% of pitch, bars inside the plot band
- carries: one per gap between adjacent bars, at the level it transports
  (+/- 0.75px), spanning the full gap (right edge to left edge, +/- 1px),
  declaring that running total in data-carry, stroke clearing 3:1 against
  paper
- labels: every bar prints its value in mono 8px - totals/subtotals and
  increases above the bar top (baseline top - 8), decreases below the bar
  bottom (baseline bottom + 12), deltas with an explicit sign, totals
  unsigned
- sign treatment: increases rgba(muted,0.15) fill + muted 1px stroke,
  decreases hollow (paper fill) + muted 1px stroke, totals/subtotals
  rgba(ink,0.08) fill + ink 1px stroke, at most one focal bridge with
  rgba(accent,0.12) fill + accent 1px stroke
- fail closed: a rect inside the plot band that is neither a declared bar nor
  the paper-mask twin of one is an undeclared bar

Scope treaty: this gate's vocabulary is data-role / data-value / data-name on
<rect> and data-carry on <line>. A file carrying none of them exits 0 with no
findings. It never reads data-value on <circle> (beeswarm), data-x/data-y/
data-size (bubble), data-share (treemap), data-series (slopegraph), data-bins
(ridgeline) or data-ranks (bump).

Assumptions (pinned here, contract leaves them open):
- Skin tokens: light paper #f5f5f5 / ink #2d3142 / muted #4f5d75 / accent
  #eb6c36; dark paper #2d3142 / ink #f5f5f5 / muted #bfc0c0 / accent #f08a59
  (the dark set derived from type-bar.md § Dumbbell "Dark theme"; the
  waterfall md ships no dark tokens of its own). Treatment colours are
  role-resolved through these tokens and compared per channel (+/-1) with
  alpha +/-0.01.
- Paper = the first rect covering >= 50% of the viewBox with a solid parsed
  fill; without it the decrease-fill and carry-contrast checks fail closed
  under paper_undetectable.
- Tick labels: mono 8px numeric texts at x in [66, 78]; each is paired with a
  full-width horizontal line within 6px of its baseline and the LINE's y is
  the scale point; unpaired labels use their own baseline.
- "ceil rounds up past hi" is checked as ceil >= hi; truncation means floor
  above 0 when lo >= 0, ceil below hi, or the bracket case failing to contain
  the data. Domain tolerance 1e-6 * max(1, hi - lo).
- The zero line must be a horizontal line at the scaled zero spanning >= 800px
  at the axis-line weight (stroke-width 1 +/- 0.1); a 0.8px gridline does not
  satisfy it.
- Conservation compares declared values exactly (1e-9); geometry tolerances
  are 0.75px (contract) for levels and 0.01px for grid/pitch equality.
- A label belongs to a bar when its parsed value equals the bar's declared
  value and its x sits within the bar's width (+8px slack); the nearest
  baseline wins when several match.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = ("data-role", "data-value", "data-name", "data-carry")

PLOT_X0, PLOT_X1 = 80.0, 960.0
PLOT_Y0, PLOT_Y1 = 40.0, 420.0
PLOT_H = PLOT_Y1 - PLOT_Y0
GRID = 4.0
GEOM_TOL = 0.75
POINT_TOL = 0.5
GRID_TOL = 0.01
CARRY_X_TOL = 1.0
LABEL_BASELINE_TOL = 2.0
LABEL_X_SLACK = 8.0
VALUE_EPS = 1e-9
CONTRAST_MIN = 3.0
CONTRAST_EPS = 1e-9
ZERO_LINE_MIN_SPAN = 800.0
ROLES = ("total", "delta", "subtotal")
SIGNED_RE = re.compile(r"^[+\-\u2212]")

SKIN_TOKENS = {
    "light": {
        "ink": (45.0, 49.0, 66.0),
        "muted": (79.0, 93.0, 117.0),
        "accent": (235.0, 108.0, 54.0),
    },
    "dark": {
        "ink": (245.0, 245.0, 245.0),
        "muted": (191.0, 192.0, 192.0),
        "accent": (240.0, 138.0, 89.0),
    },
}
TOTAL_FILL_ALPHA = 0.08
INCREASE_FILL_ALPHA = 0.15
FOCAL_FILL_ALPHA = 0.12
ALPHA_TOL = 0.01
CHANNEL_TOL = 1.0
STROKE_W = 1.0
STROKE_W_TOL = 0.05

HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$"
)
NUMBER_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
MONO_RE = re.compile(r"mono", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.strip())
    except ValueError:
        return None


def text_of(el: ET.Element) -> str:
    return "".join(el.itertext()).strip()


def describe(el: ET.Element) -> str:
    attrs = " ".join(f'{k}="{el.get(k)}"' for k in VOCAB if el.get(k) is not None)
    ident = el.get("id")
    if ident:
        attrs = (attrs + f' id="{ident}"').strip()
    return f"<{local_name(el.tag)}{' ' + attrs if attrs else ''}>"


def parse_number(text: str | None) -> float | None:
    if text is None:
        return None
    candidate = text.strip().replace("\u2212", "-")
    if not NUMBER_RE.match(candidate):
        return None
    return float(candidate)


def sign_prefix(raw: str) -> tuple[bool, bool]:
    """(starts with '+', starts with '-' or U+2212) on the stripped text."""
    stripped = raw.strip()
    return stripped.startswith("+"), stripped[:1] in ("-", "\u2212")


def parse_color(value: str | None) -> tuple[tuple[float, float, float], float] | None:
    if value is None:
        return None
    value = value.strip()
    match = HEX6_RE.match(value)
    if match:
        digits = match.group(1)
        return (
            (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)),
            1.0,
        )
    match = HEX3_RE.match(value)
    if match:
        digits = match.group(1)
        return (
            (int(digits[0] * 2, 16), int(digits[1] * 2, 16), int(digits[2] * 2, 16)),
            1.0,
        )
    match = RGBA_RE.match(value)
    if match:
        alpha = 1.0 if match.group(4) is None else float(match.group(4))
        return (
            (float(match.group(1)), float(match.group(2)), float(match.group(3))),
            alpha,
        )
    return None


def srgb_to_linear(channel: float) -> float:
    c = channel / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def composite(
    fg: tuple[float, float, float], alpha: float, bg: tuple[float, float, float]
) -> tuple[float, float, float]:
    return tuple(alpha * f + (1.0 - alpha) * b for f, b in zip(fg, bg))  # type: ignore[return-value]


def on_paper(
    color: tuple[tuple[float, float, float], float], paper: tuple[float, float, float]
) -> tuple[float, float, float]:
    return composite(color[0], color[1], paper)


def viewBox_of(root: ET.Element) -> tuple[float, float, float, float]:
    parts = (root.get("viewBox") or "").replace(",", " ").split()
    if len(parts) == 4:
        values = [parse_float(p) for p in parts]
        if all(v is not None for v in values):
            return tuple(values)  # type: ignore[return-value]
    return (0.0, 0.0, 1000.0, 500.0)


def detect_paper(root: ET.Element) -> tuple[float, float, float] | None:
    _, _, vb_w, vb_h = viewBox_of(root)
    vb_area = vb_w * vb_h
    for el in root.iter():
        if local_name(el.tag) != "rect":
            continue
        color = parse_color(el.get("fill"))
        if color is None or color[1] < 0.999:
            continue
        w = parse_float(el.get("width"))
        h = parse_float(el.get("height"))
        if w is None or h is None:
            continue
        if w * h >= 0.5 * vb_area:
            return color[0]
    return None


def is_mono_8(el: ET.Element) -> bool:
    size = parse_float(el.get("font-size"))
    family = el.get("font-family") or ""
    return size is not None and abs(size - 8.0) <= 0.01 and bool(MONO_RE.search(family))


def fit_line(points: list[tuple[float, float]]) -> tuple[float, float] | None:
    n = len(points)
    if n < 2:
        return None
    mean_v = sum(p[0] for p in points) / n
    mean_d = sum(p[1] for p in points) / n
    denom = sum((p[0] - mean_v) ** 2 for p in points)
    if denom <= 1e-12:
        return None
    b = sum((p[0] - mean_v) * (p[1] - mean_d) for p in points) / denom
    return (mean_d - b * mean_v, b)


def near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def color_near(
    parsed: tuple[tuple[float, float, float], float] | None,
    rgb: tuple[float, float, float],
    alpha: float | None = None,
) -> bool:
    if parsed is None:
        return False
    if any(abs(c - t) > CHANNEL_TOL for c, t in zip(parsed[0], rgb)):
        return False
    if alpha is None:
        return True
    return abs(parsed[1] - alpha) <= ALPHA_TOL


def on_grid(value: float) -> bool:
    rem = value % GRID
    return min(rem, GRID - rem) <= GRID_TOL


def integer_px(value: float) -> bool:
    return abs(value - round(value)) <= 0.01


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    rects = [el for el in root.iter() if local_name(el.tag) == "rect"]
    lines = [el for el in root.iter() if local_name(el.tag) == "line"]
    texts = [el for el in root.iter() if local_name(el.tag) == "text"]

    bars_el = [el for el in rects if el.get("data-role") is not None]
    carries_el = [el for el in lines if el.get("data-carry") is not None]
    if not bars_el and not carries_el:
        return []  # scope treaty: not a waterfall file

    paper = detect_paper(root)
    if paper is None:
        findings.append(
            "paper_undetectable: <svg>: no paper rect (solid fill covering >= 50% of the"
            " viewBox) found; the decrease-fill and carry 3:1 checks fail closed"
        )
        tokens = SKIN_TOKENS["light"]
    else:
        tokens = SKIN_TOKENS["light" if luminance(paper) >= 0.5 else "dark"]

    # ---- declarations ----
    bars: list[dict] = []
    for el in bars_el:
        role = (el.get("data-role") or "").strip()
        value_str = el.get("data-value")
        value = parse_number(value_str)
        name = (el.get("data-name") or "").strip()
        geom = tuple(parse_float(el.get(k)) for k in ("x", "y", "width", "height"))
        bar = {
            "el": el,
            "role": role,
            "value": value,
            "value_str": value_str,
            "name": name,
            "geom": geom if all(g is not None for g in geom) else None,
            "level_before": None,
            "level_after": None,
        }
        bars.append(bar)
        if role not in ROLES:
            findings.append(
                f'bar_role_invalid: {describe(el)}: data-role="{role}" is not one of'
                " total, delta, subtotal"
            )
        if value_str is None:
            findings.append(
                f"bar_value_missing: {describe(el)}: bar declares no data-value; the"
                " machine-readable contract requires it on every bar rect"
            )
        elif value is None:
            findings.append(
                f'bar_value_unparsable: {describe(el)}: data-value="{value_str}" does not'
                " parse as a number"
            )
        else:
            starts_plus, starts_minus = sign_prefix(value_str)
            if role == "delta" and not (starts_plus or starts_minus):
                findings.append(
                    f'delta_sign_missing: {describe(el)}: data-value="{value_str}" carries'
                    " no explicit sign; deltas are explicitly signed +/-"
                )
            if role in ("total", "subtotal") and (
                starts_plus or (starts_minus and value >= 0)
            ):
                findings.append(
                    f'total_sign_unexpected: {describe(el)}: data-value="{value_str}"'
                    " carries a sign prefix; totals are unsigned (a negative total keeps"
                    " the minus that is part of the number)"
                )
        if not name:
            findings.append(
                f"name_missing: {describe(el)}: data-name is absent or empty; every bar"
                " rect declares data-name"
            )
        if bar["geom"] is None:
            findings.append(
                f"bar_geometry_unparsable: {describe(el)}: x/y/width/height do not all"
                " parse; the drawing cannot be checked against the declaration"
            )

    n = len(bars)
    if not 3 <= n <= 8:
        findings.append(
            f"bar_count: <svg>: {n} declared bars; a waterfall carries 3-8 bars total,"
            " including both totals and at most one subtotal"
        )
    totals = [b for b in bars if b["role"] == "total"]
    subtotals = [b for b in bars if b["role"] == "subtotal"]
    if len(totals) != 2:
        findings.append(
            f'total_count: <svg>: {len(totals)} bars declare data-role="total"; the walk'
            " is start total + end total, exactly two"
        )
    if len(subtotals) > 1:
        findings.append(
            f"subtotal_count: <svg>: {len(subtotals)} subtotals; a walk that needs several"
            " resting points is two walks - split it"
        )

    walk_order_ok = n >= 2
    if n >= 2:
        if bars[0]["role"] != "total" or bars[-1]["role"] != "total":
            walk_order_ok = False
            findings.append(
                "walk_order: <svg>: the first and last bars must be the start and end"
                " totals; narrative order runs start total, signed bridges, optional"
                " subtotal, end total"
            )
        for prev, curr in zip(bars, bars[1:]):
            if prev["geom"] is None or curr["geom"] is None:
                continue
            if curr["geom"][0] <= prev["geom"][0] + 0.01:
                walk_order_ok = False
                findings.append(
                    f"walk_order: {describe(curr['el'])}: bar sits at x={curr['geom'][0]:g},"
                    f" not right of the previous bar at x={prev['geom'][0]:g}; the walk"
                    " runs left -> right in narrative order"
                )

    # ---- running totals / conservation ----
    walk_ok = walk_order_ok and all(b["value"] is not None for b in bars)
    if walk_order_ok and bars and bars[0]["value"] is not None:
        if bars[0]["role"] == "total" and bars[0]["value"] <= 0:
            findings.append(
                f"start_degenerate: {describe(bars[0]['el'])}: start total is"
                f" {bars[0]['value']:g}; a degenerate start (zero or negative total) is a"
                " named failure - the scale is derived from the start anchor"
            )
    if walk_ok:
        running = bars[0]["value"]
        bars[0]["level_before"] = running
        bars[0]["level_after"] = running
        for bar in bars[1:]:
            value = bar["value"]
            if bar["role"] == "delta":
                bar["level_before"] = running
                if value == 0.0:
                    findings.append(
                        f"zero_bridge: {describe(bar['el'])}: delta declares 0; zero"
                        " bridges are dropped, never drawn - state it in prose or the"
                        " source line instead"
                    )
                running += value
                bar["level_after"] = running
            else:  # total (end) or subtotal
                bar["level_before"] = running
                bar["level_after"] = running
                if not near(value, running, VALUE_EPS):
                    rule = (
                        "conservation_end"
                        if bar["role"] == "total"
                        else "conservation_subtotal"
                    )
                    findings.append(
                        f"{rule}: {describe(bar['el'])}: declares {value:g} but the running"
                        f" total walking from the start anchor is {running:g}; start +"
                        " every signed bridge = each subtotal and the end total, exactly"
                        " - a waterfall that doesn't add up is not approximately right,"
                        " it is wrong"
                    )
                    running = value
                    bar["level_after"] = running

    levels = [
        lev
        for bar in bars
        for lev in (bar["level_before"], bar["level_after"])
        if lev is not None
    ]

    # ---- shared scale ----
    tick_points: list[tuple[float, float]] = []
    for el in texts:
        if not is_mono_8(el):
            continue
        x = parse_float(el.get("x"))
        baseline = parse_float(el.get("y"))
        if x is None or baseline is None or not (66.0 <= x <= 78.0):
            continue
        value = parse_number(text_of(el))
        if value is None:
            continue
        line_y = None
        for ln in lines:
            g = [parse_float(ln.get(k)) for k in ("x1", "y1", "x2", "y2")]
            if any(v is None for v in g):
                continue
            x1, y1, x2, y2 = g  # type: ignore[misc]
            if abs(y1 - y2) > 0.01:
                continue
            if abs(x1 - PLOT_X0) > 2.0 or abs(x2 - PLOT_X1) > 2.0:
                continue
            if abs(y1 - baseline) <= 6.0:
                line_y = y1
                break
        tick_points.append((value, line_y if line_y is not None else baseline))

    scale: tuple[float, float] | None = None
    if len({v for v, _ in tick_points}) >= 2:
        fit = fit_line(tick_points)
        if fit is None:
            findings.append(
                "scale_unverifiable: <svg>: tick labels are degenerate (all at one"
                " position); the shared scale cannot be fitted"
            )
        else:
            a, b = fit
            if b >= -1e-12:
                findings.append(
                    f"scale_direction: <svg>: fitted tick scale runs {b:g} px per unit; the"
                    " value axis must decrease in y as values grow"
                )
            else:
                for value, y in tick_points:
                    if abs(y - (a + b * value)) > POINT_TOL:
                        findings.append(
                            f'tick_off_scale: <text> "{value:g}" pairs at y={y:g}; the'
                            f" fitted shared scale puts it at {a + b * value:.1f}"
                        )
                scale = (a, b)
    else:
        # Refit from the start anchor: floor = 0, k from the start bar's drawn top.
        start = bars[0] if bars else None
        fallback_sound = (
            walk_ok
            and start is not None
            and start["role"] == "total"
            and start["value"] is not None
            and start["value"] > 0
            and start["geom"] is not None
            and levels
            and min(levels) >= 0.0
        )
        if fallback_sound:
            k = (PLOT_Y1 - start["geom"][1]) / start["value"]
            if k > 1e-12:
                scale = (PLOT_Y1, -k)
        if scale is None:
            findings.append(
                "scale_unverifiable: <svg>: fewer than two distinct numeric tick labels"
                " and the start anchor cannot refit the scale (needs a positive start"
                " total, sound walk and non-negative levels); geometry and domain cannot"
                " be proved"
            )

    floor = ceil = None
    if scale is not None:
        a, b = scale
        floor = (PLOT_Y1 - a) / b
        ceil = (PLOT_Y0 - a) / b

    # ---- domain sign cases ----
    if scale is not None and levels and floor is not None and ceil is not None:
        lo, hi = min(levels), max(levels)
        dom_tol = 1e-6 * max(1.0, hi - lo)
        if ceil - floor <= dom_tol:
            findings.append(
                f"domain_degenerate: <svg>: fitted domain [{floor:g},{ceil:g}] has no"
                " span; the all-zero fallback span is floor=0, ceil=1"
            )
        elif lo == 0.0 and hi == 0.0:
            if abs(floor) > dom_tol or abs(ceil - 1.0) > dom_tol:
                findings.append(
                    f"domain_all_zero_fallback: <svg>: every level is zero but the fitted"
                    f" domain is [{floor:g},{ceil:g}]; the fallback span is floor=0,"
                    " ceil=1 in the data's unit"
                )
        elif lo >= 0.0:
            if abs(floor) > dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: lo={lo:g} >= 0 anchors floor=0, but the"
                    f" fitted floor is {floor:g}; the domain follows the data's range,"
                    " never its observed extremes - a waterfall on a clipped domain"
                    " inflates every bridge"
                )
            if ceil < hi - dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: hi={hi:g} exceeds the fitted ceil={ceil:g};"
                    " ceil rounds up past hi"
                )
        elif hi <= 0.0:
            if abs(ceil) > dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: hi={hi:g} <= 0 anchors ceil=0, but the"
                    f" fitted ceil is {ceil:g}"
                )
            if floor > lo + dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: lo={lo:g} falls below the fitted floor"
                    f"={floor:g}; floor rounds down past lo"
                )
        else:
            if floor > lo + dom_tol or ceil < hi - dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: levels span [{lo:g},{hi:g}] but the fitted"
                    f" domain is [{floor:g},{ceil:g}]; lo < 0 < hi brackets both sides"
                )
            a, b = scale
            zero_y = a + b * 0.0
            has_zero_line = False
            for ln in lines:
                g = [parse_float(ln.get(k)) for k in ("x1", "y1", "x2", "y2")]
                if any(v is None for v in g):
                    continue
                x1, y1, x2, y2 = g  # type: ignore[misc]
                if abs(y1 - y2) > 0.01 or abs(y1 - zero_y) > POINT_TOL:
                    continue
                if abs(x2 - x1) < ZERO_LINE_MIN_SPAN:
                    continue
                width = parse_float(ln.get("stroke-width"))
                if width is not None and abs(width - 1.0) <= 0.1:
                    has_zero_line = True
                    break
            if not has_zero_line:
                findings.append(
                    f"zero_line_missing: <svg>: zero falls inside the plot at y={zero_y:.1f}"
                    " but no full-width line in the axis-line weight marks it; zero is"
                    " what every bridge is read against"
                )

    # ---- geometry ----
    geomed = [b for b in bars if b["geom"] is not None]
    for bar in geomed:
        el = bar["el"]
        x, y, w, h = bar["geom"]
        if not on_grid(x) or not on_grid(w):
            findings.append(
                f"grid_snap: {describe(el)}: x={x:g}, width={w:g}; bar x-positions and"
                " widths are layout, so they stay on the 4px grid"
            )
        if not integer_px(y) or not integer_px(h):
            findings.append(
                f"pixel_rounding: {describe(el)}: y={y:g}, height={h:g}; endpoint positions"
                " round to the nearest integer pixel and never snap to the 4px grid"
            )
        if (
            x < PLOT_X0 - 0.01
            or x + w > PLOT_X1 + 0.01
            or y < PLOT_Y0 - GEOM_TOL
            or y + h > PLOT_Y1 + GEOM_TOL
        ):
            findings.append(
                f"bar_out_of_band: {describe(el)}: bar spans x [{x:g},{x + w:g}],"
                f" y [{y:g},{y + h:g}]; the plot band is x 80->960, y 40->420"
            )
        if scale is not None and bar["level_before"] is not None:
            a, b = scale
            if bar["role"] in ("total", "subtotal"):
                expected_top = a + b * bar["level_before"]
                if not near(y + h, PLOT_Y1, GEOM_TOL) or not near(
                    y, expected_top, GEOM_TOL
                ):
                    findings.append(
                        f"total_geometry: {describe(el)}: drawn y={y:g}, bottom={y + h:g};"
                        f" a total anchors at the baseline y=420 and rises to its level"
                        f" {bar['level_before']:g} at y={expected_top:.1f} (+/-0.75px)"
                    )
            elif bar["role"] == "delta" and bar["level_after"] is not None:
                top_level = max(bar["level_before"], bar["level_after"])
                bottom_level = min(bar["level_before"], bar["level_after"])
                expected_top = a + b * top_level
                expected_bottom = a + b * bottom_level
                if not near(y, expected_top, GEOM_TOL) or not near(
                    y + h, expected_bottom, GEOM_TOL
                ):
                    findings.append(
                        f"bridge_geometry: {describe(el)}: drawn y={y:g}, bottom={y + h:g};"
                        f" the bridge must span exactly its two running levels"
                        f" {bottom_level:g}..{top_level:g} at y={expected_top:.1f}.."
                        f"{expected_bottom:.1f} (+/-0.75px) - stretching one bridge for"
                        " legibility moves money that doesn't exist"
                    )
    if len(geomed) >= 2:
        widths = [b["geom"][2] for b in geomed]
        xs = [b["geom"][0] for b in geomed]
        if max(widths) - min(widths) > GRID_TOL:
            findings.append(
                "bar_pitch: <svg>: bar widths differ"
                f" ({min(widths):g}..{max(widths):g}); equal-width bars on an even pitch"
            )
        pitches = [j - i for i, j in zip(xs, xs[1:])]
        if max(pitches) - min(pitches) > GRID_TOL:
            findings.append(
                "bar_pitch: <svg>: bar pitches differ"
                f" ({min(pitches):g}..{max(pitches):g}); equal-width bars on an even pitch"
            )
        elif pitches and widths:
            pitch = pitches[0]
            if widths[0] < 0.5 * pitch - GRID_TOL:
                findings.append(
                    f"bar_width_ratio: <svg>: bar width {widths[0]:g} is under 50% of the"
                    f" pitch {pitch:g}; the gap should never exceed the bar"
                )

    # ---- sign treatment ----
    focal_count = 0
    if paper is not None:
        for bar in bars:
            el = bar["el"]
            role = bar["role"]
            fill = parse_color(el.get("fill"))
            stroke = parse_color(el.get("stroke"))
            stroke_w = parse_float(el.get("stroke-width"))
            stroke_ok = (
                stroke_w is not None and abs(stroke_w - STROKE_W) <= STROKE_W_TOL
            )
            is_accent_stroke = color_near(stroke, tokens["accent"])
            if role in ("total", "subtotal"):
                if not (
                    color_near(fill, tokens["ink"], TOTAL_FILL_ALPHA)
                    and color_near(stroke, tokens["ink"])
                    and stroke_ok
                ):
                    findings.append(
                        f"total_treatment: {describe(el)}: totals are the heaviest marks -"
                        f" rgba(ink,0.08) fill with a 1px ink stroke; found fill="
                        f'"{el.get("fill")}" stroke="{el.get("stroke")}"'
                        f' stroke-width="{el.get("stroke-width")}"'
                    )
            elif role == "delta" and bar["value"] is not None:
                if is_accent_stroke:
                    focal_count += 1
                    if not (
                        color_near(fill, tokens["accent"], FOCAL_FILL_ALPHA)
                        and stroke_ok
                    ):
                        findings.append(
                            f"focal_treatment: {describe(el)}: the focal bridge takes"
                            f" rgba(accent,0.12) fill with an accent 1px stroke; found"
                            f' fill="{el.get("fill")}" stroke-width='
                            f'"{el.get("stroke-width")}"'
                        )
                elif bar["value"] > 0:
                    if not (
                        color_near(fill, tokens["muted"], INCREASE_FILL_ALPHA)
                        and color_near(stroke, tokens["muted"])
                        and stroke_ok
                    ):
                        findings.append(
                            f"sign_treatment_increase: {describe(el)}: increases take the"
                            f" bar family's default tint - rgba(muted,0.15) fill, muted 1px"
                            f' stroke; found fill="{el.get("fill")}" stroke='
                            f'"{el.get("stroke")}" stroke-width="{el.get("stroke-width")}"'
                        )
                elif bar["value"] < 0:
                    if not (
                        color_near(fill, paper)
                        and fill is not None
                        and fill[1] >= 0.999
                        and color_near(stroke, tokens["muted"])
                        and stroke_ok
                    ):
                        findings.append(
                            f"sign_treatment_decrease: {describe(el)}: decreases are hollow"
                            f" - paper fill, muted 1px stroke; found fill="
                            f'"{el.get("fill")}" stroke="{el.get("stroke")}"'
                            f' stroke-width="{el.get("stroke-width")}" - sign is encoded'
                            " by fill weight, not hue"
                        )
    if focal_count > 1:
        findings.append(
            f"focal_count: <svg>: {focal_count} bars carry the accent focal treatment; at"
            " most one focal bridge, and it replaces that bar's sign fill"
        )

    # ---- carries ----
    if n >= 2 and scale is not None and walk_ok:
        a, b = scale
        gaps = []
        for i in range(n - 1):
            level = bars[i]["level_after"]
            if level is None or bars[i]["geom"] is None or bars[i + 1]["geom"] is None:
                gaps.append(None)
                continue
            x1 = bars[i]["geom"][0] + bars[i]["geom"][2]
            x2 = bars[i + 1]["geom"][0]
            gaps.append((level, a + b * level, x1, x2))
        assigned: dict[int, list[ET.Element]] = {i: [] for i in range(len(gaps))}
        for el in carries_el:
            g = [parse_float(el.get(k)) for k in ("x1", "y1", "x2", "y2")]
            if any(v is None for v in g):
                findings.append(
                    f"carry_unmatched: {describe(el)}: carry endpoints do not parse"
                )
                continue
            mid = (g[0] + g[2]) / 2.0  # type: ignore[operator]
            best, best_dist = None, None
            for i, gap in enumerate(gaps):
                if gap is None:
                    continue
                _, _, x1, x2 = gap
                dist = abs(mid - (x1 + x2) / 2.0)
                if best_dist is None or dist < best_dist:
                    best, best_dist = i, dist
            if best is None:
                findings.append(
                    f"carry_unmatched: {describe(el)}: carry sits in no gap between"
                    " adjacent bars"
                )
                continue
            assigned[best].append(el)
        for i, gap in enumerate(gaps):
            if gap is None:
                continue
            level, expected_y, x1, x2 = gap
            if not assigned[i]:
                findings.append(
                    f"carry_missing: <svg>: no carry crosses the gap between bar"
                    f" {i + 1} and bar {i + 2} at level {level:g}; a floating bar with no"
                    " carry is bars at odd heights - the connector is the claim that the"
                    " total is conserved across the gap"
                )
                continue
            for extra in assigned[i][1:]:
                findings.append(
                    f"carry_unmatched: {describe(extra)}: gap {i + 1} already carries"
                    f" {describe(assigned[i][0])}; one carry per gap"
                )
            el = assigned[i][0]
            carry_value = parse_number(el.get("data-carry"))
            if carry_value is None:
                findings.append(
                    f'carry_value: {describe(el)}: data-carry="{el.get("data-carry")}"'
                    " does not parse; each carry declares the running total it transports"
                )
            elif not near(carry_value, level, VALUE_EPS):
                findings.append(
                    f"carry_value: {describe(el)}: declares {carry_value:g} but transports"
                    f" level {level:g}; a carry drawn at the wrong height reconnects the"
                    " walk to a different total"
                )
            g = [parse_float(el.get(k)) for k in ("x1", "y1", "x2", "y2")]
            cx1, cy1, cx2, cy2 = g  # type: ignore[misc]
            if abs(cy1 - cy2) > 0.01 or not near(cy1, expected_y, GEOM_TOL):
                findings.append(
                    f"carry_level: {describe(el)}: drawn at y={cy1:g}; level {level:g} sits"
                    f" at y={expected_y:.1f} (+/-0.75px) - every carry sits at the level it"
                    " transports"
                )
            if not near(cx1, x1, CARRY_X_TOL) or not near(cx2, x2, CARRY_X_TOL):
                findings.append(
                    f"carry_span: {describe(el)}: spans x [{cx1:g},{cx2:g}]; the gap runs"
                    f" [{x1:g},{x2:g}] - the carry spans its full gap, from the right edge"
                    " of one bar to the left edge of the next"
                )
            if paper is not None:
                stroke = parse_color(el.get("stroke"))
                if stroke is None:
                    findings.append(
                        f"carry_contrast: {describe(el)}: cannot parse stroke="
                        f'"{el.get("stroke")}"; the 3:1 assertion fails closed'
                    )
                else:
                    ratio = contrast(on_paper(stroke, paper), paper)
                    if ratio + CONTRAST_EPS < CONTRAST_MIN:
                        findings.append(
                            f"carry_contrast: {describe(el)}: stroke measures {ratio:.2f}:1"
                            f" against paper; the carry is load-bearing and must clear"
                            f" >= {CONTRAST_MIN:.0f}:1, not the 0.25 axis hairline"
                        )

    # ---- labels ----
    label_pool = [el for el in texts if is_mono_8(el)]
    for bar in bars:
        el = bar["el"]
        if bar["value"] is None or bar["geom"] is None:
            continue
        x, y, w, h = bar["geom"]
        centre = x + w / 2.0
        decrease = bar["role"] == "delta" and bar["value"] < 0
        expected_baseline = (y + h + 12.0) if decrease else (y - 8.0)
        candidates = []
        for lab in label_pool:
            lx = parse_float(lab.get("x"))
            ly = parse_float(lab.get("y"))
            if lx is None or ly is None or abs(lx - centre) > w / 2.0 + LABEL_X_SLACK:
                continue
            value = parse_number(text_of(lab))
            if value is None or not near(value, bar["value"], VALUE_EPS):
                continue
            candidates.append((abs(ly - expected_baseline), ly, lab))
        if not candidates:
            findings.append(
                f"value_label_missing: {describe(el)}: no mono 8px label printing"
                f" {bar['value']:g} over the bar; every bar prints its value"
            )
            continue
        candidates.sort(key=lambda item: item[0])
        _, baseline, lab = candidates[0]
        if abs(baseline - expected_baseline) > LABEL_BASELINE_TOL:
            findings.append(
                f"label_position: {describe(lab)}: baseline y={baseline:g}; "
                + (
                    f"a decrease prints below the bar bottom (baseline {expected_baseline:g})"
                    if decrease
                    else f"totals and increases print above the bar top (baseline {expected_baseline:g})"
                )
            )
        raw = text_of(lab)
        has_sign = bool(SIGNED_RE.match(raw))
        if bar["role"] == "delta" and not has_sign:
            findings.append(
                f'label_sign_missing: {describe(lab)}: prints "{raw}"; deltas print with'
                " an explicit sign (+/-) - an unsigned bridge asks the reader to infer"
                " direction from geometry alone"
            )
        if bar["role"] in ("total", "subtotal") and has_sign:
            findings.append(
                f'label_sign_unexpected: {describe(lab)}: prints "{raw}"; totals print'
                " unsigned"
            )

    # ---- undeclared bars ----
    declared_geom = [b["geom"] for b in bars if b["geom"] is not None]
    for el in rects:
        if el.get("data-role") is not None:
            continue
        geom = tuple(parse_float(el.get(k)) for k in ("x", "y", "width", "height"))
        if any(g is None for g in geom):
            continue
        x, y, w, h = geom  # type: ignore[misc]
        if w <= 0 or h <= 0:
            continue
        if (
            x < PLOT_X0 - 0.01
            or x + w > PLOT_X1 + 0.01
            or y < PLOT_Y0 - 0.01
            or y + h > PLOT_Y1 + 0.01
        ):
            continue
        twin = any(
            near(x, dg[0], 0.01)
            and near(y, dg[1], 0.01)
            and near(w, dg[2], 0.01)
            and near(h, dg[3], 0.01)
            for dg in declared_geom
        )
        if twin:
            continue  # paper mask
        findings.append(
            f"undeclared_bar: {describe(el)}: rect at ({x:g},{y:g}) {w:g}x{h:g} inside the"
            " plot band is neither a declared bar nor a declared bar's paper-mask twin;"
            " every bar rect declares data-role, data-value and data-name"
        )

    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a waterfall SVG against references/type-waterfall.md."
    )
    parser.add_argument("svg_file", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = ET.parse(args.svg_file).getroot()
    except (ET.ParseError, OSError) as error:
        print(f"parse_error: {error}")
        return 1
    findings = check(root)
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
