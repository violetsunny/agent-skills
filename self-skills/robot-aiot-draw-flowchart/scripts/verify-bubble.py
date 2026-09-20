#!/usr/bin/env python3
"""Gate for the bubble variant of the Scatter Plot type.

Contract source: references/type-scatter.md, section "Bubble"
(honest-data rule, "Declaring the values", layout conventions, colour,
anti-patterns).

Checks implemented:
- item count 5-15 (below 5 the leave-one-out scale check has nothing to hold
  onto; above 15 the reading degrades to a density cloud)
- area encodes the third value, never radius: one constant K with
  r = K*sqrt(size) across the figure, derived from the set itself
  (Theil-Sen, leave-one-out); radius-proportional sizing fails the residual
  check because r = c*v is not linear in sqrt(v)
- one linear scale per axis, derived from the set itself (Theil-Sen,
  leave-one-out); every bubble centre sits on both
- data-size must be positive: a non-positive magnitude cannot be a bubble
- at most one accent bubble (fill hue deviating from the modal ink hue)
- paint order on every overlapping pair: the larger bubble is declared first
- data-name on every data circle, non-empty and unique
- bound labels (data-name + data-role="label") capped at four (the focal
  plus at most 2-3 outliers), each naming exactly one bubble and printing
  that name
- bound ticks (data-tick x/y + data-value): 4-6 per axis at equal intervals,
  printed text equal to the binding, position on the derived axis scale
- transform refused on bubbles, bound labels, bound ticks, ancestor <g> and
  in CSS (attribute, inline style, or <style> rule)

Scope treaty: this gate reads data-x/data-y/data-size on <circle> elements
(its own vocabulary) and never reads data-series (the slopegraph's binding),
data-value on circles (beeswarm), data-bins (ridgeline) or data-ranks (bump).
data-value on <text> ticks is shared with the beeswarm contract and is read
only inside a file this gate already claims. A file with no data-size/data-x/
data-y circle belongs to a sibling gate: exit 0 with no findings and no
mention of foreign vocabulary, so neither gate claims the other's file.

Assumptions (the contract leaves these open):
- Residual tolerance is 0.5px for both axis scales and the area fit; the
  Theil-Sen intercept of the (sqrt(size), r) fit must additionally be within
  0.5px of zero, because r = K*sqrt(v) + a with a != 0 breaks the
  area-proportional claim even when the slope is consistent.
- The full-set fit is computed first; leave-one-out refits run only when
  some bubble exceeds the tolerance against the full fit.
- Overlap means centre distance < r1 + r2 - 0.01; document order is the
  element order of root.iter(). Equal-radius overlaps carry no order
  requirement.
- The accent bubble is a bubble whose fill hue (rgb, ignoring alpha) differs
  from the modal fill hue; the ink opacity ramp varies alpha only.
- Label text is compared to data-name case-insensitively (small-caps
  printing); the label cap is pinned at 4 (focal + at most 3 outliers).
- Tick value equality is float equality between the printed number and
  data-value; equal intervals are compared in value space (1e-6 relative).
- Paper underlay circles carry no bindings and are ignored entirely.
- Any `transform` declaration inside <style> or inside an inline style of a
  bound element or ancestor is rejected wholesale: CSS selectors are not
  resolved, because transforms are rejected rather than resolved.
"""

from __future__ import annotations

import argparse
import math
import re
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = (
    "data-name",
    "data-x",
    "data-y",
    "data-size",
    "data-role",
    "data-tick",
    "data-value",
)
BUBBLE_VOCAB = ("data-name", "data-x", "data-y", "data-size")

MIN_BUBBLES = 5
MAX_BUBBLES = 15
MAX_LABELS = 4
MIN_TICKS = 4
MAX_TICKS = 6
POINT_TOL = 0.5
OVERLAP_EPS = 0.01
NUM_TOKEN_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$"
)
HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")
TRANSFORM_RE = re.compile(r"(?<![-\w])transform\s*:")


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


def parse_color(value: str | None) -> tuple[float, float, float] | None:
    if not value:
        return None
    v = value.strip()
    m = RGBA_RE.match(v)
    if m:
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)))
    m = HEX6_RE.match(v)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    m = HEX3_RE.match(v)
    if m:
        h = m.group(1)
        return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16))
    return None


def theil_sen(points: list[tuple[float, float]]) -> tuple[float, float] | None:
    slopes = []
    n = len(points)
    for i in range(n):
        vi, pi = points[i]
        for j in range(i + 1, n):
            vj, pj = points[j]
            dv = vj - vi
            if abs(dv) > 1e-12:
                slopes.append((pj - pi) / dv)
    if not slopes:
        return None
    b = statistics.median(slopes)
    a = statistics.median([p - b * v for v, p in points])
    return (a, b)


def axis_findings(
    bubbles: list[dict], key: str, coord: str, rule: str, findings: list[str]
) -> tuple[float, float] | None:
    usable = [b for b in bubbles if b[key] is not None and b[coord] is not None]
    points = [(b[key], b[coord]) for b in usable]
    fit = theil_sen(points)
    if fit is None:
        if len(usable) >= 2:
            findings.append(
                f"{rule}: <svg>: bubbles carry fewer than two distinct {key} values; the shared"
                f" {key} scale cannot be derived from the set"
            )
        return None
    a, b = fit
    flagged = [x for x in usable if abs(x[coord] - (a + b * x[key])) > POINT_TOL]
    if not flagged:
        return fit
    for k, x in enumerate(usable):
        others = points[:k] + points[k + 1 :]
        loo = theil_sen(others) or fit
        expected = loo[0] + loo[1] * x[key]
        if abs(x[coord] - expected) > POINT_TOL:
            findings.append(
                f"{rule}: {describe(x['el'])}: {coord}={x[coord]:g} is off the shared {key} scale"
                f" (expected {expected:.3f} for {key}={x[key]:g}, leave-one-out fit); a bubble"
                " nudged aside reads as a different number"
            )
    return fit


def area_findings(bubbles: list[dict], findings: list[str]) -> None:
    usable = [
        b
        for b in bubbles
        if b["size"] is not None and b["size"] > 0 and b["r"] is not None
    ]
    points = [(math.sqrt(b["size"]), b["r"]) for b in usable]
    fit = theil_sen(points)
    if fit is None:
        if len(usable) >= 2:
            findings.append(
                "area_scale_unverifiable: <svg>: bubbles carry fewer than two distinct sizes;"
                " the area constant cannot be derived from the set"
            )
        return
    a, k = fit
    if abs(a) > POINT_TOL:
        findings.append(
            f"area_intercept: <svg>: the (sqrt(size), r) fit has intercept {a:.3f}px; area"
            " encodes the third value only when r = K*sqrt(size) with no additive offset"
        )
    flagged = [
        b for b in usable if abs(b["r"] - (a + k * math.sqrt(b["size"]))) > POINT_TOL
    ]
    if not flagged:
        return
    for i, b in enumerate(usable):
        others = points[:i] + points[i + 1 :]
        loo = theil_sen(others) or fit
        expected = loo[0] + loo[1] * math.sqrt(b["size"])
        if abs(b["r"] - expected) > POINT_TOL:
            findings.append(
                f"area_off_scale: {describe(b['el'])}: r={b['r']:g} is off the shared area scale"
                f" (expected {expected:.3f} for size {b['size']:g}, leave-one-out fit);"
                " radius-proportional sizing squares the claim"
            )


def transform_findings(root: ET.Element, bound: list[ET.Element]) -> list[str]:
    findings = []
    parents = {child: parent for parent in root.iter() for child in parent}
    reported: set[int] = set()
    for el in bound:
        if el.get("transform") is not None:
            findings.append(
                f"transform_forbidden: {describe(el)}: transform on a bound element moves the"
                " rendered mark away from the verified coordinate; bake the offset into cx/cy"
            )
        style = el.get("style")
        if style and TRANSFORM_RE.search(style):
            findings.append(
                f"transform_forbidden: {describe(el)}: inline style declares a transform; the"
                " checker reads raw cx/cy/r and x/y attributes"
            )
        anc = parents.get(el)
        while anc is not None:
            if id(anc) not in reported:
                reported.add(id(anc))
                if anc.get("transform") is not None:
                    findings.append(
                        f"transform_forbidden: {describe(anc)}: transform on an ancestor of bound"
                        " elements moves every verified coordinate below it"
                    )
                anc_style = anc.get("style")
                if anc_style and TRANSFORM_RE.search(anc_style):
                    findings.append(
                        f"transform_forbidden: {describe(anc)}: inline style on an ancestor of"
                        " bound elements declares a transform"
                    )
            anc = parents.get(anc)
    for el in root.iter():
        if local_name(el.tag) == "style" and el.text and TRANSFORM_RE.search(el.text):
            findings.append(
                "transform_forbidden: <style>: CSS transform rule; transforms are rejected"
                " rather than resolved, so no CSS may move verified geometry"
            )
    return findings


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    doc_index = {id(el): i for i, el in enumerate(root.iter())}

    bubbles: list[dict] = []
    for el in root.iter():
        if local_name(el.tag) != "circle":
            continue
        if not any(el.get(a) is not None for a in ("data-size", "data-x", "data-y")):
            continue
        missing = [a for a in BUBBLE_VOCAB if el.get(a) is None]
        if missing:
            findings.append(
                f"binding_bubble_incomplete: {describe(el)}: data circle is missing"
                f" {', '.join(missing)}; an unnamed bubble drops out of every comparison silently"
            )
        b = {
            "el": el,
            "name": el.get("data-name"),
            "vx": parse_float(el.get("data-x")),
            "vy": parse_float(el.get("data-y")),
            "size": parse_float(el.get("data-size")),
            "cx": parse_float(el.get("cx")),
            "cy": parse_float(el.get("cy")),
            "r": parse_float(el.get("r")),
            "fill": el.get("fill"),
        }
        for attr in ("data-x", "data-y", "data-size"):
            raw = el.get(attr)
            if raw is not None and parse_float(raw) is None:
                findings.append(
                    f"binding_value_unparsable: {describe(el)}: {attr} must be a number"
                )
        if b["cx"] is None or b["cy"] is None or b["r"] is None:
            findings.append(
                f"geometry_unparsable: {describe(el)}: cx/cy/r must be numbers"
            )
        if b["size"] is not None and b["size"] <= 0:
            findings.append(
                f"size_nonpositive: {describe(el)}: data-size={b['size']:g}; area has no sign -"
                " omit the item and say so"
            )
        bubbles.append(b)

    if not bubbles:
        return []

    n = len(bubbles)
    if not MIN_BUBBLES <= n <= MAX_BUBBLES:
        findings.append(
            f"bubble_count: <svg>: {n} data circles; the bubble contract requires"
            f" {MIN_BUBBLES}-{MAX_BUBBLES}"
        )

    names: dict[str, list[dict]] = {}
    for b in bubbles:
        if b["name"] is None or not b["name"].strip():
            if b["name"] is not None:
                findings.append(
                    f"name_empty: {describe(b['el'])}: data-name is empty; an unnamed bubble"
                    " cannot be labelled or cross-checked"
                )
            continue
        names.setdefault(b["name"], []).append(b)
    for name, group in names.items():
        if len(group) > 1:
            findings.append(
                f"name_duplicate: {describe(group[-1]['el'])}: data-name '{name}' is carried by"
                f" {len(group)} bubbles; two bubbles sharing a name collapse into one entry"
            )

    fit_x = axis_findings(bubbles, "vx", "cx", "x_off_scale", findings)
    fit_y = axis_findings(bubbles, "vy", "cy", "y_off_scale", findings)
    area_findings(bubbles, findings)

    hues: dict[tuple, list[dict]] = {}
    for b in bubbles:
        rgb = parse_color(b["fill"])
        if rgb is not None:
            hues.setdefault(rgb, []).append(b)
    if len(hues) > 1:
        modal = max(hues.values(), key=len)
        accents = [b for group in hues.values() if group is not modal for b in group]
        if len(accents) > 1:
            findings.append(
                f"accent_cap: <svg>: {len(accents)} bubbles deviate from the ink ramp hue; one"
                " accent bubble, and an ink opacity ramp for everything else - never a hue per item"
            )

    geo = [
        b
        for b in bubbles
        if b["cx"] is not None and b["cy"] is not None and b["r"] is not None
    ]
    for i in range(len(geo)):
        for j in range(i + 1, len(geo)):
            a, b = geo[i], geo[j]
            dist = math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"])
            if dist < a["r"] + b["r"] - OVERLAP_EPS and a["r"] != b["r"]:
                larger, smaller = (a, b) if a["r"] > b["r"] else (b, a)
                if doc_index[id(larger["el"])] > doc_index[id(smaller["el"])]:
                    findings.append(
                        f"paint_order: {describe(larger['el'])}: bubble r={larger['r']:g} overlaps"
                        f" bubble r={smaller['r']:g} but is painted later; draw order is largest"
                        " first - a small bubble painted early is buried under a later giant"
                    )

    bound: list[ET.Element] = [b["el"] for b in bubbles]

    labels: list[ET.Element] = []
    ticks: list[dict] = []
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        if el.get("data-tick") is not None:
            ticks.append({"el": el})
        elif el.get("data-name") is not None:
            labels.append(el)
    bound.extend(t["el"] for t in ticks)
    bound.extend(labels)

    if len(labels) > MAX_LABELS:
        findings.append(
            f"label_cap: <svg>: {len(labels)} bound labels; the focal bubble plus at most 2-3"
            f" outliers, no more than {MAX_LABELS} - never all of them"
        )
    for el in labels:
        if el.get("data-role") != "label":
            findings.append(
                f"label_binding_incomplete: {describe(el)}: a bound label requires"
                ' data-role="label" alongside data-name'
            )
            continue
        name = el.get("data-name", "")
        if not name.strip():
            findings.append(
                f"name_empty: {describe(el)}: data-name is empty; the label floats free"
            )
            continue
        if name not in names:
            findings.append(
                f"label_target_unknown: {describe(el)}: no bubble declares data-name='{name}'; a"
                " label could name a bubble that is not there"
            )
            continue
        if len(names[name]) != 1:
            continue
        visible = text_of(el)
        if visible.casefold() != name.casefold():
            findings.append(
                f"label_text_mismatch: {describe(el)}: printed {visible!r} != bound name {name!r}"
            )

    per_axis: dict[str, list[dict]] = {"x": [], "y": []}
    for t in ticks:
        el = t["el"]
        axis = el.get("data-tick")
        if axis not in per_axis:
            findings.append(
                f"tick_axis_unknown: {describe(el)}: data-tick must be 'x' or 'y'"
            )
            continue
        raw = el.get("data-value")
        value = parse_float(raw)
        if raw is None:
            findings.append(
                f"tick_binding_incomplete: {describe(el)}: a bound tick requires data-value"
            )
            continue
        if value is None:
            findings.append(
                f"binding_value_unparsable: {describe(el)}: data-value must be a number"
            )
            continue
        t["value"] = value
        t["axis"] = axis
        per_axis[axis].append(t)
        visible = text_of(el)
        tokens = NUM_TOKEN_RE.findall(visible)
        if len(tokens) != 1 or float(tokens[0].replace(",", "")) != value:
            findings.append(
                f"tick_text_mismatch: {describe(el)}: printed {visible!r} != bound data-value"
                f" {raw!r}; the printed axis could be relabelled wholesale"
            )
        fit = fit_x if axis == "x" else fit_y
        coord = parse_float(el.get(axis))
        if coord is None:
            findings.append(
                f"geometry_unparsable: {describe(el)}: {axis} must be a number"
            )
        elif fit is not None and abs(coord - (fit[0] + fit[1] * value)) > POINT_TOL:
            findings.append(
                f"tick_off_scale: {describe(el)}: {axis}-tick at {coord:g} is off the shared"
                f" {axis} scale (expected {fit[0] + fit[1] * value:.3f} for value {value:g})"
            )

    for axis, group in per_axis.items():
        if not group:
            continue
        if not MIN_TICKS <= len(group) <= MAX_TICKS:
            findings.append(
                f"tick_count: <svg>: {len(group)} bound {axis}-ticks; the bubble contract"
                f" requires {MIN_TICKS}-{MAX_TICKS} per axis"
            )
        if len(group) >= 3:
            values = sorted(t["value"] for t in group)
            gaps = [b - a for a, b in zip(values, values[1:])]
            span = max(abs(v) for v in values) or 1.0
            if max(gaps) - min(gaps) > 1e-6 * span:
                findings.append(
                    f"tick_spacing: <svg>: bound {axis}-ticks are not at equal intervals (gaps"
                    f" {', '.join(f'{g:g}' for g in gaps)})"
                )

    findings.extend(transform_findings(root, bound))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a bubble chart SVG against references/type-scatter.md."
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
