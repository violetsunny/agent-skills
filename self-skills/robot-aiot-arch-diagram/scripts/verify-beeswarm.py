#!/usr/bin/env python3
"""Gate for the beeswarm variant of the Scatter Plot type.

Contract source: references/type-scatter.md, section "Beeswarm"
(honest-data rule, "Declaring the values", layout conventions, colour,
anti-patterns).

Checks implemented:
- dot count 20-300 (both ends of the budget enforced)
- one linear value scale derived from the dots themselves (Theil-Sen,
  leave-one-out, so one dishonest dot cannot drag the line it is measured
  against); every dot's cx must sit on it
- dots sharing a value share a position on the value axis
- no two dots overprint (centre distance >= r1 + r2)
- every dot at one radius; the focal dot keeps the shared radius
- every non-focal dot at one literally identical fill; at most one accent dot
- data-name non-empty and unique to one dot
- bound labels (data-name + data-role="label") capped at six, each naming
  exactly one dot and printing that name
- bound ticks (data-tick="x" + data-value): 4-6 at equal intervals, printed
  text equal to the binding, position on the derived scale
- positioning carriers refused on dots, bound labels, bound ticks, ancestor
  <g>/<svg> and in <style>: the transform attribute, inline style, and the
  positioning properties transform/translate/rotate/scale, the SVG geometry
  properties cx/cy/r/x/y, and CSS motion path

Scope treaty: this gate reads data-value on <circle> elements (its own
vocabulary) and never reads data-series (slopegraph), data-bins (ridgeline),
data-ranks (bump) or data-size (bubble). Detection is element-scoped:
data-value also appears on <text> axis ticks in the bubble contract, so only
a <circle> binding it puts a file inside this gate. A file with no
data-value circle belongs to a sibling gate: exit 0 with no findings and no
mention of foreign vocabulary, so neither gate claims the other's file.

Assumptions (the contract leaves these open):
- Scale residual tolerance is 0.5px (the house tolerance). The full-set
  Theil-Sen fit is computed first; the leave-one-out refits run only when
  some dot exceeds the tolerance against the full fit, which keeps the
  honest common case linear-time in pairs while preserving the guarantee
  that one dishonest dot cannot drag the line.
- "Share a position" on the value axis means equal cx within 0.01px; the
  swarm-axis coordinate (cy) is packing and is never checked.
- Overprint means centre distance < r1 + r2 - 0.01; touching is allowed.
- Radius equality tolerance is 0.01px.
- The accent dot is the single dot whose fill deviates from the modal
  non-focal fill; a deviating fill on a dot without a non-empty data-name
  is a non-focal fill violation instead, because the focal dot is named.
- Label text is compared to data-name case-insensitively: the shipped
  grammar prints small-caps ("req-4c1f" prints "REQ-4C1F").
- Tick value equality is float equality between the printed number and
  data-value; equal intervals are compared in value space (1e-6 relative).
- A <circle> carrying data-name but no data-value is legend scenery, not a
  dot, and is ignored.
- Any positioning property inside <style> is rejected wholesale: CSS
  selectors are not resolved, because carriers are rejected rather than
  resolved. Inline style attributes are checked against the same property
  list; line-height, color and font declarations do not move anything and
  stay legal.
"""

from __future__ import annotations

import argparse
import math
import re
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = ("data-value", "data-name", "data-role", "data-tick")

MIN_DOTS = 20
MAX_DOTS = 300
MAX_LABELS = 6
MIN_TICKS = 4
MAX_TICKS = 6
POINT_TOL = 0.5
SAME_POS_TOL = 0.01
RADIUS_TOL = 0.01
OVERLAP_EPS = 0.01
NUM_TOKEN_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
TRANSFORM_RE = re.compile(r"(?<![-\w])transform\s*:")
POSITION_PROP_RE = re.compile(
    r"(?<![-\w])(?:translate|rotate|scale|cx|cy|r|x|y|offset-path|offset-distance"
    r"|offset-rotate|motion-path)\s*:"
)


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


def theil_sen(points: list[tuple[float, float]]) -> tuple[float, float] | None:
    """Theil-Sen fit p = a + b*v over (value, position) pairs; None when fewer
    than two distinct values leave no pairwise slope."""
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


def scale_off_findings(
    dots: list[dict], rule: str, findings: list[str]
) -> tuple[float, float] | None:
    """Check every dot's cx against a Theil-Sen scale with leave-one-out
    refits for any dot the full fit flags. Returns the full fit."""
    usable = [d for d in dots if d["value"] is not None and d["cx"] is not None]
    points = [(d["value"], d["cx"]) for d in usable]
    fit = theil_sen(points)
    if fit is None:
        if len(usable) >= 2:
            findings.append(
                "scale_unverifiable: <svg>: dots carry fewer than two distinct values; the"
                " shared linear scale cannot be derived from the set"
            )
        return None
    a, b = fit
    flagged = [d for d in usable if abs(d["cx"] - (a + b * d["value"])) > POINT_TOL]
    if not flagged:
        return fit
    for k, d in enumerate(usable):
        others = points[:k] + points[k + 1 :]
        loo = theil_sen(others) or fit
        la, lb = loo
        expected = la + lb * d["value"]
        if abs(d["cx"] - expected) > POINT_TOL:
            findings.append(
                f"{rule}: {describe(d['el'])}: cx={d['cx']:g} is off the shared value scale"
                f" (expected {expected:.3f} for value {d['value']:g}, leave-one-out fit);"
                " a dot nudged along the value axis is the type's one unforgivable error"
            )
    return fit


def carrier_findings(root: ET.Element, bound: list[ET.Element]) -> list[str]:
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
        if style and POSITION_PROP_RE.search(style):
            findings.append(
                f"position_forbidden: {describe(el)}: inline style declares a positioning"
                " property; nothing may position a mark except its own attributes"
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
                if anc_style and POSITION_PROP_RE.search(anc_style):
                    findings.append(
                        f"position_forbidden: {describe(anc)}: inline style on an ancestor of"
                        " bound elements declares a positioning property"
                    )
            anc = parents.get(anc)
    for el in root.iter():
        if local_name(el.tag) == "style" and el.text:
            if TRANSFORM_RE.search(el.text):
                findings.append(
                    "transform_forbidden: <style>: CSS transform rule; transforms are rejected"
                    " rather than resolved, so no CSS may move verified geometry"
                )
            if POSITION_PROP_RE.search(el.text):
                findings.append(
                    "position_forbidden: <style>: CSS rule declares a positioning property"
                    " (translate/rotate/scale, a geometry property, or a motion path); CSS beats"
                    " the presentation attribute, so no CSS may move verified geometry"
                )
    return findings


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    dots: list[dict] = []
    for el in root.iter():
        if local_name(el.tag) == "circle" and el.get("data-value") is not None:
            dots.append({"el": el})
    if not dots:
        return findings

    for d in dots:
        el = d["el"]
        d["value"] = parse_float(el.get("data-value"))
        d["cx"] = parse_float(el.get("cx"))
        d["cy"] = parse_float(el.get("cy"))
        d["r"] = parse_float(el.get("r"))
        d["fill"] = el.get("fill")
        d["name"] = el.get("data-name")
        if d["value"] is None:
            findings.append(
                f"binding_value_unparsable: {describe(el)}: data-value must be a number"
            )
        if d["cx"] is None or d["cy"] is None or d["r"] is None:
            findings.append(
                f"geometry_unparsable: {describe(el)}: cx/cy/r must be numbers"
            )

    n = len(dots)
    if not MIN_DOTS <= n <= MAX_DOTS:
        findings.append(
            f"dot_count: <svg>: {n} dots; the beeswarm contract requires {MIN_DOTS}-{MAX_DOTS}"
            " - below 20 there is no distribution to swarm, above 300 bin into a histogram"
        )

    fit = scale_off_findings(dots, "value_off_scale", findings)

    by_value: dict[float, list[dict]] = {}
    for d in dots:
        if d["value"] is not None and d["cx"] is not None:
            by_value.setdefault(d["value"], []).append(d)
    for value, group in sorted(by_value.items()):
        cxs = [d["cx"] for d in group]
        if len(group) > 1 and max(cxs) - min(cxs) > SAME_POS_TOL:
            findings.append(
                f"same_value_position: {describe(group[-1]['el'])}: dots sharing value"
                f" {value:g} must share a position on the value axis, found cx"
                f" {', '.join(f'{x:g}' for x in sorted(set(cxs)))}; two items with one value"
                " share a position and dodge apart"
            )

    geo = [
        d
        for d in dots
        if d["cx"] is not None and d["cy"] is not None and d["r"] is not None
    ]
    for i in range(len(geo)):
        for j in range(i + 1, len(geo)):
            a, b = geo[i], geo[j]
            dist = math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"])
            if dist < a["r"] + b["r"] - OVERLAP_EPS:
                findings.append(
                    f"overprint: {describe(b['el'])}: dot at ({b['cx']:g},{b['cy']:g}) overprints the"
                    f" dot at ({a['cx']:g},{a['cy']:g}) ({dist:.3f}px apart, radii sum"
                    f" {a['r'] + b['r']:g}); a dot painted over another turns density into darkness"
                )

    radii = [d["r"] for d in dots if d["r"] is not None]
    if radii:
        mode_r = statistics.mode(radii)
        for d in dots:
            if d["r"] is not None and abs(d["r"] - mode_r) > RADIUS_TOL:
                findings.append(
                    f"dot_radius: {describe(d['el'])}: r={d['r']:g} deviates from the shared radius"
                    f" {mode_r:g}; the focal dot keeps the shared radius - a bigger focal dot is a"
                    " second encoding and breaks the packing"
                )

    fills = [d["fill"] for d in dots if d["fill"] is not None]
    if fills:
        mode_fill = statistics.mode(fills)
        deviants = [d for d in dots if d["fill"] is not None and d["fill"] != mode_fill]
        if len(deviants) > 1:
            findings.append(
                f"accent_cap: <svg>: {len(deviants)} dots deviate from the single non-focal fill;"
                " at most one accent dot - groups are a facet decision, not a palette decision"
            )
        for d in deviants:
            if not (d["name"] is not None and d["name"].strip()):
                findings.append(
                    f"nonfocal_fill: {describe(d['el'])}: fill {d['fill']!r} deviates from the"
                    f" literally identical non-focal fill {mode_fill!r} on an unnamed dot; density"
                    " must read as swarm thickness, never as tone"
                )

    names: dict[str, list[dict]] = {}
    for d in dots:
        if d["name"] is None:
            continue
        if not d["name"].strip():
            findings.append(
                f"name_empty: {describe(d['el'])}: data-name is empty; a name that identifies no"
                " mark identifies neither"
            )
            continue
        names.setdefault(d["name"], []).append(d)
    for name, group in names.items():
        if len(group) > 1:
            findings.append(
                f"name_duplicate: {describe(group[-1]['el'])}: data-name '{name}' is carried by"
                f" {len(group)} dots; two dots sharing a name collapse into one entry, so a single"
                " label satisfies both"
            )

    bound: list[ET.Element] = [d["el"] for d in dots]

    labels: list[dict] = []
    ticks: list[dict] = []
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        if el.get("data-tick") is not None:
            ticks.append({"el": el})
        elif el.get("data-name") is not None:
            labels.append({"el": el})
    bound.extend(t["el"] for t in ticks)
    bound.extend(l["el"] for l in labels)

    if len(labels) > MAX_LABELS:
        findings.append(
            f"label_cap: <svg>: {len(labels)} bound labels; the beeswarm contract allows the focal"
            f" dot plus the outliers a reader will look for, at most {MAX_LABELS}"
        )
    for l in labels:
        el = l["el"]
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
                f"label_target_unknown: {describe(el)}: no dot declares data-name='{name}'; a label"
                " could name a dot that is not there"
            )
            continue
        if len(names[name]) != 1:
            continue
        visible = text_of(el)
        if visible.casefold() != name.casefold():
            findings.append(
                f"label_text_mismatch: {describe(el)}: printed {visible!r} != bound name {name!r}"
            )

    for t in ticks:
        el = t["el"]
        if el.get("data-tick") != "x":
            findings.append(
                f"tick_axis_unknown: {describe(el)}: data-tick must be 'x'; the beeswarm has one"
                " horizontal value axis"
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
        visible = text_of(el)
        tokens = NUM_TOKEN_RE.findall(visible)
        if len(tokens) != 1 or float(tokens[0].replace(",", "")) != value:
            findings.append(
                f"tick_text_mismatch: {describe(el)}: printed {visible!r} != bound data-value"
                f" {raw!r}; the printed axis could be relabelled wholesale"
            )
        tx = parse_float(el.get("x"))
        if tx is None:
            findings.append(f"geometry_unparsable: {describe(el)}: x must be a number")
        elif fit is not None and abs(tx - (fit[0] + fit[1] * value)) > POINT_TOL:
            findings.append(
                f"tick_off_scale: {describe(el)}: tick x={tx:g} is off the shared value scale"
                f" (expected {fit[0] + fit[1] * value:.3f} for value {value:g})"
            )

    usable_ticks = [
        t
        for t in ticks
        if t.get("value") is not None and t.get("el").get("data-tick") == "x"
    ]
    if ticks and not MIN_TICKS <= len(usable_ticks) <= MAX_TICKS:
        findings.append(
            f"tick_count: <svg>: {len(usable_ticks)} bound ticks; the beeswarm contract requires"
            f" {MIN_TICKS}-{MAX_TICKS}"
        )
    if len(usable_ticks) >= 3:
        values = sorted(t["value"] for t in usable_ticks)
        gaps = [b - a for a, b in zip(values, values[1:])]
        span = max(abs(v) for v in values) or 1.0
        if max(gaps) - min(gaps) > 1e-6 * span:
            findings.append(
                "tick_spacing: <svg>: bound ticks are not at equal intervals (gaps"
                f" {', '.join(f'{g:g}' for g in gaps)})"
            )

    findings.extend(carrier_findings(root, bound))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a beeswarm SVG against references/type-scatter.md."
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
