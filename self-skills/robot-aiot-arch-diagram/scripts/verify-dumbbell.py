#!/usr/bin/env python3
"""Gate for the Dumbbell variant of the Bar type.

Contract source: references/type-bar.md, section "Dumbbell" (layout, element
pattern, "Non-text contrast" paragraph, "Dumbbell honesty rules"):
"scripts/verify-dumbbell.py asserts all four [3:1 marks], so a later tint
change cannot quietly drop one under the line" and "scripts/verify-dumbbell.py
resolves the domain over every sign case and asserts finite coordinates and
3:1 marks". Line 100 additionally owes, for a shipped example, "a check of
drawn positions against the values printed at them" - implemented here from
the value labels.

Checks implemented:
- domain resolution over all four sign cases from the values printed at the
  dots: lo >= 0 anchors floor = 0 with ceil rounded up past hi; hi <= 0
  anchors ceil = 0 with floor rounded down past lo; lo < 0 < hi brackets
  both sides and requires the zero line at its scaled position; all-zero
  data requires the finite fallback span floor = 0, ceil = 1
- finite, non-degenerate scale fitted from the tick labels (>= 2 distinct
  numeric ticks, every tick on the fitted line, axis running left -> right)
- drawn dot positions: x = 200 + (v - floor) / (ceil - floor) * 760, rounded
  to the nearest integer pixel (<= 0.5px off, and cx integral)
- the four 3:1 non-text-contrast assertions, tokens read out of the file and
  composited on the file's own paper:
    connector stroke vs paper (>= 3.0)
    hollow endpoint's muted stroke vs paper (>= 3.0)
    solid endpoint's 1px ink stroke vs paper (>= 3.0)
    solid endpoint's stroke vs its own fill (>= 3.0)
- row integrity: every connector (horizontal line strictly inside the plot
  band) carries exactly two r=6 dots - one hollow (paper fill), one solid -
  declared after the connector so the dots cap it, the connector reaching
  both dot centres without overshooting the dots, and both dots labelled
  with their real values (two mono 8px labels on the row's baselines)

Scope treaty: this gate's vocabulary is structural - a complete dumbbell row
(a horizontal in-band line with exactly two r=6 circles centred on its span).
It deliberately reads NO data-* vocabulary: not data-series (slopegraph),
not data-bins (ridgeline), not data-ranks (bump), not data-value on circles
(beeswarm), not data-x/data-y/data-size (bubble), not data-share (treemap).
A file with no complete row exits 0 with no findings.

Assumptions (pinned here, contract leaves them open):
- Row pitch/origin table, row count cap, label offsets (x_left - 12 /
  x_right + 12, floor exception) and legend geometry are layout conventions
  the contract does not assign to this script (its own scope sentence names
  domain resolution, finite coordinates and the four 3:1 marks); they are
  left to review. The label GEOMETRY is used only to find and pair labels,
  never asserted.
- Value labels: <text> with font-size 8, a monospace family, a numeric parse
  (ASCII '-'/'+' or Unicode minus U+2212), baseline at row y+4 or (floor
  exception) y-10 within 1px, x within [140, 1020]. The two labels of a row
  pair with the two dots by x order.
- Tick labels: font-size 8 mono, numeric, baseline y=440 +/- 2, x within the
  plot span +/- 0.5; the label's own x is the tick position ("centered under
  each gridline").
- "ceil rounds up past hi" is checked as ceil >= hi (a dot may sit exactly on
  the last tick); truncation means floor > 0 when lo >= 0, ceil < hi, or the
  bracket case failing to contain zero. Domain tolerance is
  1e-6 * max(1, hi - lo); position tolerance 0.5px.
- Hollow vs solid: a dot whose fill composites to the paper colour
  (per-channel distance <= 2) is hollow; both dots hollow or both solid is a
  finding.
- Paper = the first rect covering >= 50% of the viewBox with a solid parsed
  fill. A contrast assertion whose colour cannot be parsed fails closed under
  its own rule name.
- The zero line must be a vertical line at the scaled zero spanning at least
  380px; its weight is not asserted (the contract names the axis-line weight,
  but the assertions assigned to this script are the four 3:1 marks).
- Known contract conflict (reported, not averaged away): type-bar.md line 90
  gives the dark-skin solid dot as #f08a59 with an #f5f5f5 stroke; that pair
  measures 2.27:1 stroke-vs-fill, under the 3:1 line 72 asks this script to
  assert on every skin. The gate asserts the contract text (skin-independent
  3:1) and therefore rejects the line-90 dark treatment.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB: tuple[str, ...] = ()

PLOT_X0, PLOT_X1 = 200.0, 960.0
PLOT_Y0, PLOT_Y1 = 40.0, 420.0
PLOT_W = 760.0
DOT_R = 6.0
POINT_TOL = 0.5
BASELINE_TOL = 1.0
TICK_Y = 440.0
TICK_Y_TOL = 2.0
CONTRAST_MIN = 3.0
CONTRAST_EPS = 1e-9
LABEL_X0, LABEL_X1 = PLOT_X0 - 60.0, PLOT_X1 + 60.0
ZERO_LINE_MIN_SPAN = 380.0
PAPER_CHANNEL_TOL = 2.0
GEOM_ATTRS = ("cx", "cy", "r", "x", "y", "x1", "y1", "x2", "y2")

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
    attrs = " ".join(f'{k}="{el.get(k)}"' for k in GEOM_ATTRS if el.get(k) is not None)
    ident = el.get("id")
    if ident:
        attrs = (attrs + f' id="{ident}"').strip()
    return f"<{local_name(el.tag)}{' ' + attrs if attrs else ''}>"


def parse_number(text: str) -> float | None:
    candidate = text.strip().replace("\u2212", "-")
    if not NUMBER_RE.match(candidate):
        return None
    return float(candidate)


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
        x = parse_float(el.get("x")) or 0.0
        y = parse_float(el.get("y")) or 0.0
        w = parse_float(el.get("width"))
        h = parse_float(el.get("height"))
        if w is None or h is None:
            continue
        if w * h >= 0.5 * vb_area:
            return color[0]
    return None


def font_size_of(el: ET.Element) -> float | None:
    return parse_float(el.get("font-size"))


def is_mono_8(el: ET.Element) -> bool:
    size = font_size_of(el)
    family = el.get("font-family") or ""
    return size is not None and abs(size - 8.0) <= 0.01 and bool(MONO_RE.search(family))


def fit_line(points: list[tuple[float, float]]) -> tuple[float, float] | None:
    """Least-squares fit dep = a + b * value; returns (a, b)."""
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


def stroke_vs_paper_finding(
    rule: str,
    el: ET.Element,
    raw: str | None,
    paper: tuple[float, float, float] | None,
    what: str,
) -> str | None:
    color = parse_color(raw)
    if color is None or paper is None:
        return (
            f'{rule}: {describe(el)}: cannot parse stroke="{raw}" (or the paper) - the'
            f" 3:1 assertion for {what} fails closed"
        )
    ratio = contrast(on_paper(color, paper), paper)
    if ratio + CONTRAST_EPS < CONTRAST_MIN:
        return (
            f'{rule}: {describe(el)}: stroke="{raw}" measures {ratio:.2f}:1 for {what};'
            f" WCAG 1.4.11 needs >= {CONTRAST_MIN:.0f}:1"
        )
    return None


def check(root: ET.Element) -> list[str]:
    order = {id(el): index for index, el in enumerate(root.iter())}
    lines = [el for el in root.iter() if local_name(el.tag) == "line"]
    circles = [el for el in root.iter() if local_name(el.tag) == "circle"]
    texts = [el for el in root.iter() if local_name(el.tag) == "text"]

    def circle_geom(el: ET.Element) -> tuple[float, float, float] | None:
        cx, cy, r = (parse_float(el.get(k)) for k in ("cx", "cy", "r"))
        if cx is None or cy is None or r is None:
            return None
        return (cx, cy, r)

    def line_geom(el: ET.Element) -> tuple[float, float, float, float] | None:
        x1, y1, x2, y2 = (parse_float(el.get(k)) for k in ("x1", "y1", "x2", "y2"))
        if None in (x1, y1, x2, y2):
            return None
        return (x1, y1, x2, y2)  # type: ignore[return-value]

    # Candidate connectors: horizontal lines strictly inside the plot band.
    candidates: list[tuple[ET.Element, float, float, float]] = []
    for el in lines:
        geom = line_geom(el)
        if geom is None:
            continue
        x1, y1, x2, y2 = geom
        if abs(y1 - y2) > 0.01 or not (PLOT_Y0 < y1 < PLOT_Y1):
            continue
        lo_x, hi_x = min(x1, x2), max(x1, x2)
        if lo_x < PLOT_X0 - POINT_TOL or hi_x > PLOT_X1 + POINT_TOL:
            continue
        candidates.append((el, y1, lo_x, hi_x))

    def bound_dots(y: float, lo_x: float, hi_x: float) -> list[ET.Element]:
        bound = []
        for dot in circles:
            geom = circle_geom(dot)
            if geom is None:
                continue
            cx, cy, r = geom
            if abs(r - DOT_R) > 0.01 or abs(cy - y) > POINT_TOL:
                continue
            if lo_x - DOT_R - POINT_TOL <= cx <= hi_x + DOT_R + POINT_TOL:
                bound.append(dot)
        return bound

    rows: list[tuple[ET.Element, float, list[ET.Element]]] = []
    for el, y, lo_x, hi_x in candidates:
        bound = bound_dots(y, lo_x, hi_x)
        if len(bound) == 2:
            rows.append((el, y, bound))
    if not rows:
        return []  # scope treaty: no complete dumbbell row, not this gate's file

    findings: list[str] = []
    paper = detect_paper(root)

    # Row integrity for every candidate connector, complete or not.
    for el, y, lo_x, hi_x in candidates:
        bound = bound_dots(y, lo_x, hi_x)
        if len(bound) != 2:
            findings.append(
                f"row_endpoint_count: {describe(el)}: connector at y={y:g} carries"
                f" {len(bound)} r=6 dots; a dumbbell row is exactly two - a row missing an"
                " endpoint is disclosed, never silently dropped, and a third dot makes the"
                " connector meaningless"
            )

    # Stray in-band r=6 dots not part of any complete row.
    row_dot_ids = {id(dot) for _, _, dots in rows for dot in dots}
    strays = []
    for dot in circles:
        geom = circle_geom(dot)
        if geom is None or id(dot) in row_dot_ids:
            continue
        cx, cy, r = geom
        if abs(r - DOT_R) <= 0.01 and PLOT_Y0 < cy < PLOT_Y1:
            strays.append((dot, cx, cy))
    paired_strays: set[int] = set()
    for i, (dot_a, cx_a, cy_a) in enumerate(strays):
        if id(dot_a) in paired_strays:
            continue
        for dot_b, cx_b, cy_b in strays[i + 1 :]:
            if id(dot_b) in paired_strays:
                continue
            if abs(cy_a - cy_b) <= POINT_TOL:
                paired_strays.add(id(dot_a))
                paired_strays.add(id(dot_b))
                findings.append(
                    f"connector_missing: {describe(dot_a)}: dot pair at y={cy_a:g} has no"
                    " connector line; the connector is what says these two dots are one"
                    " row, so it has to be there and to clear 3:1"
                )
                break
    for dot, cx, cy in strays:
        if id(dot) not in paired_strays:
            findings.append(
                f"row_endpoint_count: {describe(dot)}: lone r=6 dot at ({cx:g},{cy:g}); a"
                " lone dot is indistinguishable from two coincident dots - a row missing"
                " an endpoint is disclosed, never silently dropped"
            )

    # Value labels per row.
    dot_value: dict[int, float] = {}
    all_values: list[float] = []
    for line_el, y, dots in rows:
        left, right = sorted(dots, key=lambda d: circle_geom(d)[0])  # type: ignore[arg-type,return-value]
        labels = []
        for el in texts:
            if not is_mono_8(el):
                continue
            baseline = parse_float(el.get("y"))
            x = parse_float(el.get("x"))
            if baseline is None or x is None or not (LABEL_X0 <= x <= LABEL_X1):
                continue
            if (
                min(abs(baseline - (y + 4.0)), abs(baseline - (y - 10.0)))
                > BASELINE_TOL
            ):
                continue
            value = parse_number(text_of(el))
            if value is None:
                continue
            labels.append((x, el, value))
        if len(labels) < 2:
            findings.append(
                f"value_label_missing: {describe(line_el)}: row at y={y:g} prints"
                f" {len(labels)} parsable mono 8px value labels; both dots share one scale"
                " and one unit, so both endpoints must be labelled with their real values"
            )
        elif len(labels) > 2:
            findings.append(
                f"value_label_count: {describe(line_el)}: row at y={y:g} prints {len(labels)}"
                " value labels; a dumbbell row carries exactly two"
            )
        if len(labels) == 2:
            labels.sort(key=lambda item: item[0])
            for label, dot in zip(labels, (left, right)):
                dot_value[id(dot)] = label[2]
                all_values.append(label[2])

        # Hollow/solid classification and the four 3:1 assertions.
        classified = []
        for dot in (left, right):
            fill_raw = dot.get("fill")
            fill = parse_color(fill_raw)
            hollow = (
                fill is not None
                and paper is not None
                and max(abs(c - p) for c, p in zip(on_paper(fill, paper), paper))
                <= PAPER_CHANNEL_TOL
            )
            classified.append((dot, hollow))
        hollows = [dot for dot, hollow in classified if hollow]
        solids = [dot for dot, hollow in classified if not hollow]
        if len(hollows) != 1 or len(solids) != 1:
            findings.append(
                f"dot_pair_style: {describe(line_el)}: row at y={y:g} has {len(hollows)}"
                f" hollow and {len(solids)} solid dots; the reference end is hollow (paper"
                " fill, muted stroke 1.5px) and the focal end solid accent with a 1px ink"
                " stroke - fill weight, not hue, carries the pairing"
            )
        else:
            hollow_dot = hollows[0]
            solid_dot = solids[0]
            finding = stroke_vs_paper_finding(
                "hollow_dot_contrast",
                hollow_dot,
                hollow_dot.get("stroke"),
                paper,
                "the hollow endpoint's muted stroke against paper",
            )
            if finding:
                findings.append(finding)
            solid_stroke = parse_color(solid_dot.get("stroke"))
            solid_fill = parse_color(solid_dot.get("fill"))
            if solid_stroke is None or paper is None:
                findings.append(
                    f"solid_dot_stroke_paper_contrast: {describe(solid_dot)}: cannot parse"
                    f' stroke="{solid_dot.get("stroke")}" (or the paper) - the 3:1'
                    " assertion for the solid endpoint's ink stroke against paper fails"
                    " closed"
                )
            else:
                ratio = contrast(on_paper(solid_stroke, paper), paper)
                if ratio + CONTRAST_EPS < CONTRAST_MIN:
                    findings.append(
                        f"solid_dot_stroke_paper_contrast: {describe(solid_dot)}: stroke"
                        f" measures {ratio:.2f}:1 against paper; the accent fill is under"
                        f" 3:1 skin-wide, so the 1px ink stroke must clear >="
                        f" {CONTRAST_MIN:.0f}:1"
                    )
            if solid_stroke is None or solid_fill is None or paper is None:
                findings.append(
                    f"solid_dot_stroke_fill_contrast: {describe(solid_dot)}: cannot parse"
                    " stroke/fill (or the paper) - the 3:1 assertion for the solid"
                    " endpoint's stroke against its own fill fails closed"
                )
            else:
                ratio = contrast(
                    on_paper(solid_stroke, paper), on_paper(solid_fill, paper)
                )
                if ratio + CONTRAST_EPS < CONTRAST_MIN:
                    findings.append(
                        f"solid_dot_stroke_fill_contrast: {describe(solid_dot)}: stroke"
                        f" measures {ratio:.2f}:1 against its own fill; WCAG 1.4.11 needs"
                        f" >= {CONTRAST_MIN:.0f}:1"
                    )

        # Connector: paint order, span, contrast.
        if not (
            order[id(line_el)] < order[id(left)]
            and order[id(line_el)] < order[id(right)]
        ):
            findings.append(
                f"connector_paint_order: {describe(line_el)}: connector at y={y:g} is not"
                " declared before both dots; the dots cap it"
            )
        geom = line_geom(line_el)
        left_cx = circle_geom(left)[0]  # type: ignore[index]
        right_cx = circle_geom(right)[0]  # type: ignore[index]
        if geom is not None:
            x1, _, x2, _ = geom
            lo_x, hi_x = min(x1, x2), max(x1, x2)
            if not (
                left_cx - DOT_R - POINT_TOL <= lo_x <= left_cx + POINT_TOL
                and right_cx - POINT_TOL <= hi_x <= right_cx + DOT_R + POINT_TOL
            ):
                findings.append(
                    f"connector_span: {describe(line_el)}: connector spans"
                    f" [{lo_x:g},{hi_x:g}] but the dots sit at {left_cx:g} and {right_cx:g};"
                    " it must join the pair (reaching both centres) without overshooting"
                    " the dots"
                )
        finding = stroke_vs_paper_finding(
            "connector_contrast",
            line_el,
            line_el.get("stroke"),
            paper,
            "the connector against paper (the connector is the claim that these two dots"
            " are one row, so it is not the 0.25 axis hairline)",
        )
        if finding:
            findings.append(finding)

    # Scale from tick labels.
    tick_points: list[tuple[float, float]] = []
    for el in texts:
        if not is_mono_8(el):
            continue
        baseline = parse_float(el.get("y"))
        x = parse_float(el.get("x"))
        if baseline is None or x is None:
            continue
        if abs(baseline - TICK_Y) > TICK_Y_TOL or not (
            PLOT_X0 - POINT_TOL <= x <= PLOT_X1 + POINT_TOL
        ):
            continue
        value = parse_number(text_of(el))
        if value is None:
            continue
        tick_points.append((value, x))
    scale: tuple[float, float] | None = None
    if len({v for v, _ in tick_points}) < 2:
        findings.append(
            "scale_unverifiable: <svg>: fewer than two distinct numeric tick labels at"
            f" y={TICK_Y:g}; the shared scale cannot be fitted, so domain and dot positions"
            " cannot be proved finite"
        )
    else:
        fit = fit_line(tick_points)
        if fit is None:
            findings.append(
                "scale_unverifiable: <svg>: tick labels are degenerate (all at one"
                " position); the shared scale cannot be fitted"
            )
        else:
            a, b = fit
            if b <= 1e-12:
                findings.append(
                    f"scale_direction: <svg>: fitted tick scale runs {b:g} px per unit; the"
                    " value axis runs left -> right"
                )
            else:
                for value, x in tick_points:
                    if abs(x - (a + b * value)) > POINT_TOL:
                        findings.append(
                            f'tick_off_scale: <text> "{value:g}" at x={x:g}: the fitted'
                            f" shared scale puts it at {a + b * value:.1f}; all ticks sit on"
                            " one line"
                        )
                scale = (a, b)

    if scale is not None and all_values:
        a, b = scale
        floor = (PLOT_X0 - a) / b
        ceil = (PLOT_X1 - a) / b
        lo, hi = min(all_values), max(all_values)
        dom_tol = 1e-6 * max(1.0, hi - lo)
        span = ceil - floor
        if span <= dom_tol:
            findings.append(
                f"domain_degenerate: <svg>: fitted domain [{floor:g},{ceil:g}] has no span;"
                " coordinates cannot be finite - all-zero data takes the fallback span"
                " floor=0, ceil=1"
            )
        elif lo == 0.0 and hi == 0.0:
            if abs(floor) > dom_tol or abs(ceil - 1.0) > dom_tol:
                findings.append(
                    f"domain_all_zero_fallback: <svg>: every value is zero but the fitted"
                    f" domain is [{floor:g},{ceil:g}]; the fallback span is floor=0, ceil=1"
                    " in the data's unit, with every dot on the floor"
                )
        elif lo >= 0.0:
            if abs(floor) > dom_tol:
                findings.append(
                    f"domain_truncated: <svg>: lo={lo:g} >= 0 anchors floor=0, but the"
                    f" fitted floor is {floor:g}; taking min/max as the bounds IS the"
                    " truncation - narrowing the domain raises px-per-unit and draws every"
                    " gap wider"
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
                    f"domain_truncated: <svg>: data spans [{lo:g},{hi:g}] but the fitted"
                    f" domain is [{floor:g},{ceil:g}]; lo < 0 < hi brackets both sides"
                )
            zero_x = a + b * 0.0
            has_zero_line = False
            for el in lines:
                geom = line_geom(el)
                if geom is None:
                    continue
                x1, y1, x2, y2 = geom
                if abs(x1 - x2) > 0.01 or abs(x1 - zero_x) > POINT_TOL:
                    continue
                if abs(y1 - y2) >= ZERO_LINE_MIN_SPAN:
                    has_zero_line = True
                    break
            if not has_zero_line:
                findings.append(
                    f"zero_line_missing: <svg>: zero falls inside the plot at x={zero_x:.1f}"
                    " but no vertical line marks it; zero is what every gap is read"
                    " against, so it gets a line at its scaled position in the axis-line"
                    " weight"
                )

        # Drawn positions against the values printed at them.
        for dot in circles:
            if id(dot) not in dot_value:
                continue
            geom = circle_geom(dot)
            if geom is None:
                continue
            cx, _, _ = geom
            value = dot_value[id(dot)]
            expected = PLOT_X0 + (value - floor) / span * PLOT_W
            if abs(cx - expected) > POINT_TOL:
                findings.append(
                    f"dot_off_scale: {describe(dot)}: value {value:g} sits at x={cx:g} but"
                    f" the shared scale puts it at {expected:.1f} (x = 200 + (v - floor) /"
                    " (ceil - floor) * 760, rounded to the nearest integer pixel)"
                )
            if abs(cx - round(cx)) > 0.01:
                findings.append(
                    f"pixel_rounding: {describe(dot)}: cx={cx:g} is not an integer pixel;"
                    " endpoint positions round, they never snap"
                )

    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a dumbbell SVG against references/type-bar.md"
        " (Dumbbell variant)."
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
