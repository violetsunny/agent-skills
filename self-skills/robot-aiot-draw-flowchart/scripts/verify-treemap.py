#!/usr/bin/env python3
"""Gate for the Treemap type.

Contract source: references/type-treemap.md (layout conventions, "Declaring
the share", honest-data rule, anti-patterns), references/style-guide.md
("Width budget": verify-treemap.py enforces exactly the per-character text
width contract for treemap cell labels), references/output-spec.md (the same
width contract for Unicode wide/full-width characters, combining marks
non-advancing).

Checks implemented:
- every cell carries data-share, fail-closed: a rect inside the plot area
  that is not a paper-mask twin of a declared cell is a cell without its
  binding; unparsable or non-positive data-share is a finding
- cell count 4-8
- shares reconcile to 100 within display rounding, or the file discloses
  "MAY NOT SUM" in so many words
- area check as RELATIVE error ((drawn - true) / true), every cell within
  5% of its declared share
- 4px grid: cell x/y/width/height are multiples of 4; cells stay inside the
  plot area x 40->956, y 40->420
- gutters: cells must not overlap; band-adjacent cells sit exactly 4px apart
- stripe layout refused: every cell spanning the same width (or height)
  with no side-by-side neighbour is a stripe, not a squarified layout
- fill: one accent cell at most (stroke hue off the ramp); non-focal cells
  share one ink hue on fill and stroke, stroke at alpha 0.30 and 1px, focal
  stroke 1.5px; the ramp is rank-ordered (a larger share never carries a
  weaker opacity)
- labels: text width computed per the house character contract (wide/
  full-width 1em, combining marks 0, Latin advance 0.60em sans / 0.62em
  mono) must fit the cell from the 16px inset; a percentage printed inside
  a cell must match that cell's data-share at the printed precision
- info marks: a disc (circle r=5) inside the plot area must be fully
  contained by its cell, and that cell must be at least 12x12px

Scope treaty: this gate reads data-share (its own vocabulary) and never
reads data-series (slopegraph), data-from/data-to (slopegraph), data-bins
(ridgeline), data-ranks (bump), data-value on circles (beeswarm) or
data-size (bubble). A file with no data-share anywhere belongs to a sibling
gate: exit 0 with no findings and no mention of foreign vocabulary.

Assumptions (the contract leaves these open):
- "A few percent" of relative area error is pinned at 5%; the shipped
  example's worst case is 2.7%.
- Share reconciliation tolerance is 0.5 percentage points unless the file
  prints the disclosed-rounding phrase "MAY NOT SUM" (case-insensitive).
- A paper mask is a rect whose geometry exactly equals a declared cell's
  geometry; masks carry nothing and are exempt. Any other rect fully inside
  the plot area is treated as an unbound cell (fail-closed).
- Grid snap and gutter tolerances are 0.01px; adjacency for the exact-4px
  gutter means no third cell spans the gap within the pair's shared
  y-band (or x-band).
- A cell label is a <text> whose x/y anchor point falls inside the cell;
  the 16px inset applies to the left edge of the computed text box, with
  0.5px slack on both sides.
- The accent cell is identified by its stroke hue deviating from the modal
  cell stroke hue (the focal cell takes the accent stroke).
- Ramp order compares fill alpha of non-focal cells pairwise: a strictly
  larger share must carry a greater-or-equal alpha (1e-9 slack).
- Percent tokens are matched as "<number>%" inside a cell's labels; the
  printed value must equal data-share within half a unit of the printed
  precision.
"""

from __future__ import annotations

import argparse
import re
import statistics
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = ("data-share",)

PLOT_X0, PLOT_Y0, PLOT_X1, PLOT_Y1 = 40.0, 40.0, 956.0, 420.0
MIN_CELLS = 4
MAX_CELLS = 8
REL_AREA_TOL = 0.05
SUM_TOL = 0.5
GRID_TOL = 0.01
GUTTER = 4.0
INSET = 16.0
LABEL_SLACK = 0.5
DISC_R = 5.0
DISC_MIN_CELL = 12.0
STROKE_ALPHA = 0.30
DISCLOSURE_RE = re.compile(r"MAY NOT SUM", re.IGNORECASE)
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$"
)
HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")


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


def parse_color(value: str | None) -> tuple[tuple[float, float, float], float] | None:
    """Returns ((r, g, b), alpha) for rgba()/hex colors; None when unparsable."""
    if not value:
        return None
    v = value.strip()
    m = RGBA_RE.match(v)
    if m:
        alpha = 1.0 if m.group(4) is None else float(m.group(4))
        return ((float(m.group(1)), float(m.group(2)), float(m.group(3))), alpha)
    m = HEX6_RE.match(v)
    if m:
        h = m.group(1)
        return ((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)), 1.0)
    m = HEX3_RE.match(v)
    if m:
        h = m.group(1)
        return ((int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16)), 1.0)
    return None


def text_width(text: str, font_size: float, font_family: str | None) -> float:
    mono = bool(font_family and "mono" in font_family.lower())
    advance = 0.62 if mono else 0.60
    total = 0.0
    for ch in text:
        cat = unicodedata.category(ch)
        if cat in ("Mn", "Me"):
            continue
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            total += 1.0
        else:
            total += advance
    return total * font_size


def geom_of(el: ET.Element) -> tuple[float, float, float, float] | None:
    x = parse_float(el.get("x"))
    y = parse_float(el.get("y"))
    w = parse_float(el.get("width"))
    h = parse_float(el.get("height"))
    if x is None or y is None or w is None or h is None:
        return None
    return (x, y, w, h)


def in_plot(g: tuple[float, float, float, float]) -> bool:
    x, y, w, h = g
    return (
        x >= PLOT_X0 - GRID_TOL
        and y >= PLOT_Y0 - GRID_TOL
        and x + w <= PLOT_X1 + GRID_TOL
        and y + h <= PLOT_Y1 + GRID_TOL
    )


def band_overlap(a0: float, a1: float, b0: float, b1: float) -> float:
    return min(a1, b1) - max(a0, b0)


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    rects = [el for el in root.iter() if local_name(el.tag) == "rect"]
    cells = [el for el in rects if el.get("data-share") is not None]
    if not cells:
        return findings

    all_text = " ".join(
        text_of(el) for el in root.iter() if local_name(el.tag) == "text"
    )

    cell_geoms: set[tuple[float, float, float, float]] = set()
    for el in cells:
        g = geom_of(el)
        if g is not None:
            cell_geoms.add(g)

    for el in rects:
        if el.get("data-share") is not None:
            continue
        g = geom_of(el)
        if g is None or not in_plot(g):
            continue
        if g in cell_geoms:
            continue
        findings.append(
            f"cell_share_missing: {describe(el)}: rect at ({g[0]:g},{g[1]:g}) {g[2]:g}x{g[3]:g}"
            " inside the plot area carries no data-share; the gate fails closed on any cell"
            " without it - the unnamed cell is exactly the sliver the grid distorts most"
        )

    records = []
    for el in cells:
        rec = {"el": el, "geom": geom_of(el)}
        share = parse_float(el.get("data-share"))
        rec["share"] = share
        if share is None:
            findings.append(
                f"share_unparsable: {describe(el)}: data-share must be a number"
            )
        elif share <= 0:
            findings.append(
                f"share_nonpositive: {describe(el)}: data-share={share:g}; a treemap claims to"
                " show a whole, so a part must be positive - parts too small to draw get merged"
                " into one honest, named 'Other'"
            )
        if rec["geom"] is None:
            findings.append(
                f"cell_geometry: {describe(el)}: x/y/width/height must be numbers"
            )
        records.append(rec)

    n = len(records)
    if not MIN_CELLS <= n <= MAX_CELLS:
        findings.append(
            f"cell_count: <svg>: {n} cells; the treemap contract requires {MIN_CELLS}-{MAX_CELLS}"
            " - past 8 the tail becomes unlabelable slivers, group it into one named 'Other'"
        )

    shares = [r["share"] for r in records if r["share"] is not None and r["share"] > 0]
    if shares:
        total = sum(shares)
        if abs(total - 100.0) > SUM_TOL and not DISCLOSURE_RE.search(all_text):
            findings.append(
                f"shares_sum: <svg>: data-share values sum to {total:g}, not 100; either carry"
                " enough precision that the parts reconcile or say plainly in the source line"
                " that they don't (PARTS ROUNDED, MAY NOT SUM)"
            )

    geo_recs = [r for r in records if r["geom"] is not None]
    areas = [(r, r["geom"][2] * r["geom"][3]) for r in geo_recs]
    area_total = sum(a for _, a in areas)
    if area_total > 0:
        for r, area in areas:
            x, y, w, h = r["geom"]
            if not in_plot(r["geom"]):
                findings.append(
                    f"cell_bounds: {describe(r['el'])}: cell ({x:g},{y:g}) {w:g}x{h:g} leaves the"
                    f" plot area x {PLOT_X0:g}->{PLOT_X1:g}, y {PLOT_Y0:g}->{PLOT_Y1:g}"
                )
            for name, value in (("x", x), ("y", y), ("width", w), ("height", h)):
                if abs(value % 4.0) > GRID_TOL and abs(value % 4.0 - 4.0) > GRID_TOL:
                    findings.append(
                        f"grid_snap: {describe(r['el'])}: {name}={value:g} is off the 4px grid;"
                        " cell edges snap like everything else"
                    )
            if r["share"] is not None and r["share"] > 0:
                drawn = area / area_total * 100.0
                rel = (drawn - r["share"]) / r["share"]
                if abs(rel) > REL_AREA_TOL:
                    findings.append(
                        f"area_error: {describe(r['el'])}: drawn share {drawn:.3f}% vs declared"
                        f" {r['share']:g}% is a relative error of {rel * 100:+.2f}%, beyond"
                        f" {REL_AREA_TOL * 100:g}%; check the result as relative error - absolute"
                        " error hides exactly the mistake on the sliver you need to catch"
                    )

    for i in range(len(geo_recs)):
        for j in range(i + 1, len(geo_recs)):
            a = geo_recs[i]["geom"]
            b = geo_recs[j]["geom"]
            ox = band_overlap(a[0], a[0] + a[2], b[0], b[0] + b[2])
            oy = band_overlap(a[1], a[1] + a[3], b[1], b[1] + b[3])
            if ox > GRID_TOL and oy > GRID_TOL:
                findings.append(
                    f"cell_overlap: {describe(geo_recs[j]['el'])}: cell overlaps the cell at"
                    f" ({a[0]:g},{a[1]:g}); area is the only encoding and shared area double-counts"
                )
                continue
            if oy > GRID_TOL:
                left, right = (a, b) if a[0] <= b[0] else (b, a)
                gap = right[0] - (left[0] + left[2])
                between = any(
                    band_overlap(c[0], c[0] + c[2], left[0] + left[2], right[0])
                    > GRID_TOL
                    and band_overlap(
                        c[1],
                        c[1] + c[3],
                        max(a[1], b[1]),
                        min(a[1] + a[3], b[1] + b[3]),
                    )
                    > GRID_TOL
                    for c in (r["geom"] for r in geo_recs)
                    if c is not a and c is not b
                )
                if not between and abs(gap - GUTTER) > GRID_TOL:
                    findings.append(
                        f"gutter: <svg>: adjacent cells at ({left[0]:g},{left[1]:g}) and"
                        f" ({right[0]:g},{right[1]:g}) are {gap:g}px apart; the gutter between"
                        f" cells is {GUTTER:g}px"
                    )
            elif ox > GRID_TOL:
                top, bottom = (a, b) if a[1] <= b[1] else (b, a)
                gap = bottom[1] - (top[1] + top[3])
                between = any(
                    band_overlap(c[1], c[1] + c[3], top[1] + top[3], bottom[1])
                    > GRID_TOL
                    and band_overlap(
                        c[0],
                        c[0] + c[2],
                        max(a[0], b[0]),
                        min(a[0] + a[2], b[0] + b[2]),
                    )
                    > GRID_TOL
                    for c in (r["geom"] for r in geo_recs)
                    if c is not a and c is not b
                )
                if not between and abs(gap - GUTTER) > GRID_TOL:
                    findings.append(
                        f"gutter: <svg>: adjacent cells at ({top[0]:g},{top[1]:g}) and"
                        f" ({bottom[0]:g},{bottom[1]:g}) are {gap:g}px apart; the gutter between"
                        f" cells is {GUTTER:g}px"
                    )

    if len(geo_recs) >= 3:
        widths = [r["geom"][2] for r in geo_recs]
        heights = [r["geom"][3] for r in geo_recs]
        no_y_overlap = all(
            band_overlap(a[1], a[1] + a[3], b[1], b[1] + b[3]) <= GRID_TOL
            for i, a in enumerate(r["geom"] for r in geo_recs)
            for b in list(r["geom"] for r in geo_recs)[i + 1 :]
        )
        no_x_overlap = all(
            band_overlap(a[0], a[0] + a[2], b[0], b[0] + b[2]) <= GRID_TOL
            for i, a in enumerate(r["geom"] for r in geo_recs)
            for b in list(r["geom"] for r in geo_recs)[i + 1 :]
        )
        if max(widths) - min(widths) <= GRID_TOL and no_y_overlap:
            findings.append(
                "stripe_layout: <svg>: every cell spans the same width stacked in bands - simple"
                " stripes defeat area comparison; use the squarified layout"
            )
        if max(heights) - min(heights) <= GRID_TOL and no_x_overlap:
            findings.append(
                "stripe_layout: <svg>: every cell spans the same height side by side - simple"
                " stripes defeat area comparison; use the squarified layout"
            )

    for r in records:
        fill = parse_color(r["el"].get("fill"))
        stroke = parse_color(r["el"].get("stroke"))
        r["fill_rgb"] = fill[0] if fill else None
        r["fill_alpha"] = fill[1] if fill else None
        r["stroke_rgb"] = stroke[0] if stroke else None
        r["stroke_alpha"] = stroke[1] if stroke else None
        r["stroke_width"] = parse_float(r["el"].get("stroke-width"))

    stroke_hues: dict[tuple, list[dict]] = {}
    for r in records:
        if r["stroke_rgb"] is not None:
            stroke_hues.setdefault(r["stroke_rgb"], []).append(r)
    focal: list[dict] = []
    ramp: list[dict] = []
    if stroke_hues:
        modal = max(stroke_hues.values(), key=len)
        for r in records:
            (ramp if r in modal else focal).append(r)
    if len(focal) > 1:
        findings.append(
            f"accent_cap: <svg>: {len(focal)} cells carry an off-ramp stroke; one accent cell"
            " only - the editorially focal one, never a hue per cell"
        )
    for r in focal:
        if r["stroke_width"] is not None and abs(r["stroke_width"] - 1.5) > GRID_TOL:
            findings.append(
                f"focal_stroke: {describe(r['el'])}: the focal cell takes a 1.5px accent stroke,"
                f" found {r['stroke_width']:g}"
            )

    ramp_hues = {r["fill_rgb"] for r in ramp if r["fill_rgb"] is not None}
    if len(ramp_hues) > 1:
        findings.append(
            f"ramp_hue: <svg>: non-focal fills carry {len(ramp_hues)} hues; the fill is a"
            " rank-ordered ink opacity ramp - rainbow fills destroy the rank reading"
        )
    for r in ramp:
        if (
            r["fill_rgb"] is not None
            and r["stroke_rgb"] is not None
            and r["fill_rgb"] != r["stroke_rgb"]
        ):
            findings.append(
                f"ink_role: {describe(r['el'])}: fill hue {r['fill_rgb']} != stroke hue"
                f" {r['stroke_rgb']}; the hairline is the same ink role at 0.30"
            )
        if (
            r["stroke_alpha"] is not None
            and abs(r["stroke_alpha"] - STROKE_ALPHA) > GRID_TOL
        ):
            findings.append(
                f"cell_stroke: {describe(r['el'])}: non-focal stroke alpha"
                f" {r['stroke_alpha']:g} != {STROKE_ALPHA:g} (1px ink @ 0.30 hairline)"
            )
        if r["stroke_width"] is not None and abs(r["stroke_width"] - 1.0) > GRID_TOL:
            findings.append(
                f"cell_stroke: {describe(r['el'])}: non-focal stroke-width"
                f" {r['stroke_width']:g} != 1"
            )
    ordered = [
        r for r in ramp if r["share"] is not None and r["fill_alpha"] is not None
    ]
    for i in range(len(ordered)):
        for j in range(i + 1, len(ordered)):
            a, b = ordered[i], ordered[j]
            if (
                a["share"] > b["share"] + 1e-9
                and a["fill_alpha"] < b["fill_alpha"] - 1e-9
            ):
                findings.append(
                    f"ramp_order: {describe(a['el'])}: share {a['share']:g}% carries fill alpha"
                    f" {a['fill_alpha']:g} below the {b['fill_alpha']:g} of share"
                    f" {b['share']:g}%; the ramp is rank-ordered - a larger share never carries a"
                    " weaker opacity"
                )

    label_boxes = []
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        tx = parse_float(el.get("x"))
        ty = parse_float(el.get("y"))
        if tx is None or ty is None:
            continue
        for r in geo_recs:
            x, y, w, h = r["geom"]
            if (
                x - GRID_TOL <= tx <= x + w + GRID_TOL
                and y - GRID_TOL <= ty <= y + h + GRID_TOL
            ):
                label_boxes.append((r, el, tx))
                break

    for r, el, tx in label_boxes:
        x, y, w, h = r["geom"]
        visible = text_of(el)
        font_size = parse_float(el.get("font-size"))
        if font_size is not None and visible:
            width = text_width(visible, font_size, el.get("font-family"))
            anchor = el.get("text-anchor") or "start"
            if anchor == "middle":
                left = tx - width / 2
            elif anchor == "end":
                left = tx - width
            else:
                left = tx
            if left < x + INSET - LABEL_SLACK:
                findings.append(
                    f"label_inset: {describe(el)}: label box starts at {left:.2f}, inside the"
                    f" 16px inset of the cell at ({x:g},{y:g}); labels sit inside the cell,"
                    " top-left, 16px in from the edge"
                )
            if left + width > x + w + LABEL_SLACK:
                findings.append(
                    f"label_overflow: {describe(el)}: label {visible!r} computes to"
                    f" {width:.2f}px wide and crosses the cell edge at {x + w:g}; never shrink a"
                    " cell to fit its label - the cell size is the data, the label is commentary"
                )
        if r["share"] is not None:
            for token in PERCENT_RE.findall(visible):
                printed = float(token)
                decimals = len(token.split(".")[1]) if "." in token else 0
                if abs(printed - r["share"]) > 0.5 * 10 ** (-decimals) + 1e-9:
                    findings.append(
                        f"share_label_mismatch: {describe(el)}: printed {token}% != data-share"
                        f" {r['share']:g}; the label and the metadata are two statements of one"
                        " fact"
                    )

    for el in root.iter():
        if local_name(el.tag) != "circle":
            continue
        cx = parse_float(el.get("cx"))
        cy = parse_float(el.get("cy"))
        cr = parse_float(el.get("r"))
        if cx is None or cy is None or cr is None or abs(cr - DISC_R) > GRID_TOL:
            continue
        if not (PLOT_X0 <= cx <= PLOT_X1 and PLOT_Y0 <= cy <= PLOT_Y1):
            continue
        host = None
        for r in geo_recs:
            x, y, w, h = r["geom"]
            if (
                cx - cr >= x - GRID_TOL
                and cx + cr <= x + w + GRID_TOL
                and cy - cr >= y - GRID_TOL
                and cy + cr <= y + h + GRID_TOL
            ):
                host = r
                break
        if host is None:
            findings.append(
                f"marker_containment: {describe(el)}: info disc at ({cx:g},{cy:g}) r={cr:g} is"
                " not fully contained by any cell; a fixed-size disc must never cross the cell"
                " boundary"
            )
            continue
        x, y, w, h = host["geom"]
        if w < DISC_MIN_CELL - GRID_TOL or h < DISC_MIN_CELL - GRID_TOL:
            findings.append(
                f"marker_cell_too_small: {describe(el)}: info disc sits in a cell {w:g}x{h:g};"
                " below 12px on either axis the in-cell mark is omitted and the sliver is"
                " identified by position in the legend"
            )

    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a treemap SVG against references/type-treemap.md."
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
