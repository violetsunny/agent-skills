#!/usr/bin/env python3
"""Gate for the slopegraph variant of the Line Chart type.

Contract source: references/type-line.md, section "Variants > Slopegraph"
(honest-data rule, "Declaring the values", anti-patterns).

Checks implemented:
- both value axes carry the same scale and the same origin, tested
  separately (a shared origin shift tilts every slope while series still
  rank correctly, so scale and origin get their own findings)
- every endpoint sits on the shared value->y mapping
- binding completeness: data-series/data-from/data-to on series lines,
  data-series/data-end (plus data-role="name" on names) on labels,
  data-axis/data-state on state captions
- every bound visible string cross-checked against its binding
- one complete number per value label: a unit suffix is allowed, a
  thousands separator that changes the value or a second number is a finding
- label attribution: a label drawn nearer another series' endpoint than its
  own is reported
- endpoint label crowding, and series coincident at both endpoints
- transform rejected on series lines, bound labels, ancestor <g> and CSS

Scope treaty: this gate reads data-from/data-to (its own vocabulary). A file
carrying neither belongs to a sibling gate (ridgeline reads data-bins, bump
reads data-ranks): exit 0 with no findings and no mention of foreign
vocabulary, so neither gate claims the other's file.

Assumptions (the contract leaves these open):
- Axis columns are derived from the series lines' shared x1/x2, not from
  layout constants, so a resized plot needs no constant changed here.
- Tolerances: 0.5px for endpoint-on-scale residuals and for the origin
  comparison at the domain midpoint; the scale comparison allows 1.0px of
  disagreement across the full value domain.
- Label crowding threshold is 10px of vertical separation at one end;
  endpoints within 0.5px at both ends are coincident series.
- A value label must contain exactly one numeric token; comma grouping must
  be canonical (###,###); the parsed number must equal the binding exactly
  (float equality), per "round once, then draw from the rounded number".
- Any `transform` declaration inside <style> is rejected wholesale: CSS
  selectors are not resolved, because transforms are rejected rather than
  resolved. The rotated value-axis caption stays legal because it carries no
  binding attributes.
- A text element carrying data-axis/data-state is a state caption; other
  text elements are checked only when they carry slopegraph vocabulary.
- Exactly one caption per axis is required, and every series needs four
  labels: name and value at both ends.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = (
    "data-series",
    "data-from",
    "data-to",
    "data-end",
    "data-role",
    "data-axis",
    "data-state",
)
LINE_VOCAB = ("data-series", "data-from", "data-to")
NUM_TOKEN_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
CANONICAL_COMMA_RE = re.compile(r"^[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?$")

POINT_TOL = 0.5
SCALE_TOL_PX = 1.0
CROWD_PX = 10.0
COINCIDE_TOL = 0.5
AXIS_X_TOL = 0.5
MIN_SERIES = 4
MAX_SERIES = 10


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


def fit_line(points: list[tuple[float, float]]) -> tuple[float, float] | None:
    """Least-squares y = a + b*x; None when x is degenerate or too few points."""
    n = len(points)
    if n < 2:
        return None
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points)
    if sxx <= 1e-12:
        return None
    b = sum((p[0] - mx) * (p[1] - my) for p in points) / sxx
    return (my - b * mx, b)


def axis_fit(
    points: list[tuple[float, float]], fallback_b: float
) -> tuple[float, float] | None:
    fit = fit_line(points)
    if fit is not None:
        return fit
    if not points:
        return None
    mv = sum(p[0] for p in points) / len(points)
    my = sum(p[1] for p in points) / len(points)
    return (my - fallback_b * mv, fallback_b)


def token_value(token: str) -> tuple[float | None, str | None]:
    if "," in token:
        if not CANONICAL_COMMA_RE.match(token):
            return (
                None,
                f"thousands separator in {token!r} is not canonical grouping and can change the value",
            )
        return float(token.replace(",", "")), None
    return float(token), None


def transform_findings(root: ET.Element) -> list[str]:
    findings = []
    parents = {child: parent for parent in root.iter() for child in parent}
    reported: set[int] = set()
    for el in root.iter():
        if not any(el.get(a) is not None for a in VOCAB):
            continue
        if el.get("transform") is not None:
            findings.append(
                f"transform_forbidden: {describe(el)}: transform on a bound element moves the"
                " rendered mark away from the verified coordinate; bake the offset into x/y"
            )
        anc = parents.get(el)
        while anc is not None:
            if id(anc) not in reported and anc.get("transform") is not None:
                reported.add(id(anc))
                findings.append(
                    f"transform_forbidden: {describe(anc)}: transform on an ancestor of bound"
                    " elements moves every verified coordinate below it"
                )
            anc = parents.get(anc)
    for el in root.iter():
        if (
            local_name(el.tag) == "style"
            and el.text
            and re.search(r"transform\s*:", el.text)
        ):
            findings.append(
                "transform_forbidden: <style>: CSS transform rule; transforms are rejected"
                " rather than resolved, so no CSS may move verified geometry"
            )
    return findings


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    if not any(
        el.get("data-from") is not None or el.get("data-to") is not None
        for el in root.iter()
    ):
        return findings

    series: dict[str, dict] = {}
    order: list[str] = []
    for el in root.iter():
        if local_name(el.tag) != "line":
            continue
        if not any(el.get(a) is not None for a in LINE_VOCAB):
            continue
        missing = [a for a in LINE_VOCAB if el.get(a) is None]
        if missing:
            findings.append(
                f"binding_line_incomplete: {describe(el)}: series line is missing {', '.join(missing)}"
            )
            continue
        name = el.get("data-series", "")
        v_from = parse_float(el.get("data-from"))
        v_to = parse_float(el.get("data-to"))
        if v_from is None or v_to is None:
            findings.append(
                f"binding_value_unparsable: {describe(el)}: data-from/data-to must be numbers"
            )
        geo = [parse_float(el.get(a)) for a in ("x1", "y1", "x2", "y2")]
        if any(g is None for g in geo):
            findings.append(
                f"geometry_unparsable: {describe(el)}: x1/y1/x2/y2 must be numbers"
            )
            continue
        if name in series:
            findings.append(
                f"duplicate_series: {describe(el)}: series '{name}' is declared twice"
            )
            continue
        x1, y1, x2, y2 = geo  # type: ignore[misc]
        series[name] = {
            "el": el,
            "v_from": v_from,
            "v_to": v_to,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        }
        order.append(name)

    count = len(series)
    if count and not MIN_SERIES <= count <= MAX_SERIES:
        findings.append(
            f"series_count: <svg>: {count} series declared; the slopegraph contract"
            f" requires {MIN_SERIES}-{MAX_SERIES}"
        )

    axis_x: dict[str, float] = {}
    if series:
        ref = series[order[0]]
        axis_x = {"from": ref["x1"], "to": ref["x2"]}
        if ref["x1"] >= ref["x2"]:
            findings.append(
                f"axis_x_mismatch: {describe(ref['el'])}: the from-axis column must be left of the to-axis column"
            )
        for name in order[1:]:
            s = series[name]
            if (
                abs(s["x1"] - ref["x1"]) > AXIS_X_TOL
                or abs(s["x2"] - ref["x2"]) > AXIS_X_TOL
            ):
                findings.append(
                    f"axis_x_mismatch: {describe(s['el'])}: series endpoints must sit on the two shared"
                    f" axis columns (x={ref['x1']:g} and x={ref['x2']:g})"
                )

    usable = [
        s for s in series.values() if s["v_from"] is not None and s["v_to"] is not None
    ]
    from_pts = [(s["v_from"], s["y1"]) for s in usable]
    to_pts = [(s["v_to"], s["y2"]) for s in usable]
    all_pts = from_pts + to_pts
    global_fit = fit_line(all_pts)
    if usable and global_fit is None:
        findings.append(
            "scale_unverifiable: <svg>: endpoints carry fewer than two distinct values;"
            " the shared scale cannot be derived"
        )
    if global_fit is not None:
        a_g, b_g = global_fit
        fit_f = axis_fit(from_pts, b_g)
        fit_t = axis_fit(to_pts, b_g)
        if fit_f is not None and fit_t is not None:
            a_f, b_f = fit_f
            a_t, b_t = fit_t
            v_min = min(v for v, _ in all_pts)
            v_max = max(v for v, _ in all_pts)
            span = max(v_max - v_min, 1.0)
            v_mid = (v_min + v_max) / 2
            if abs(b_f - b_t) * span > SCALE_TOL_PX:
                findings.append(
                    f"axis_scale_mismatch: <svg>: from-axis scale {b_f:.6g}px/unit vs to-axis"
                    f" {b_t:.6g}px/unit; differing scales make the angle of every line fiction"
                )
            if abs((a_f + b_f * v_mid) - (a_t + b_t * v_mid)) > POINT_TOL:
                findings.append(
                    f"axis_origin_mismatch: <svg>: the two axes disagree about their origin"
                    f" ({a_f + b_f * v_mid:.3f}px vs {a_t + b_t * v_mid:.3f}px at value"
                    f" {v_mid:g}); a shared origin shift tilts every slope"
                )
        for s in usable:
            for end, v, y in (
                ("from", s["v_from"], s["y1"]),
                ("to", s["v_to"], s["y2"]),
            ):
                expected = a_g + b_g * v
                if abs(y - expected) > POINT_TOL:
                    findings.append(
                        f"endpoint_off_scale: {describe(s['el'])}: {end} endpoint y={y:g} is off the"
                        f" shared value scale (expected {expected:.3f} for value {v:g})"
                    )

    captions: dict[str, list[ET.Element]] = {"from": [], "to": []}
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        has_axis = el.get("data-axis") is not None
        has_state = el.get("data-state") is not None
        if not (has_axis or has_state):
            continue
        if not (has_axis and has_state):
            findings.append(
                f"caption_binding: {describe(el)}: a state caption requires both data-axis and data-state"
            )
            continue
        axis = el.get("data-axis", "")
        if axis not in captions:
            findings.append(
                f"caption_binding: {describe(el)}: data-axis must be 'from' or 'to'"
            )
            continue
        state = el.get("data-state", "")
        if text_of(el) != state:
            findings.append(
                f"caption_text_mismatch: {describe(el)}: visible text {text_of(el)!r} != data-state {state!r}"
            )
        cx = parse_float(el.get("x"))
        if axis_x and cx is not None and abs(cx - axis_x[axis]) > POINT_TOL:
            findings.append(
                f"caption_position: {describe(el)}: caption x={cx:g} is not on the {axis}-axis"
                f" column x={axis_x[axis]:g}; swapped captions reverse every slope"
            )
        captions[axis].append(el)
    for axis in ("from", "to"):
        if not captions[axis]:
            findings.append(
                f"caption_missing: <svg>: no state caption is bound with data-axis='{axis}'"
            )
        elif len(captions[axis]) > 1:
            findings.append(
                f"caption_duplicate: <svg>: {len(captions[axis])} captions are bound with data-axis='{axis}'"
            )

    labels: dict[tuple[str, str, str], list[ET.Element]] = {}
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        if el.get("data-axis") is not None or el.get("data-state") is not None:
            continue
        if not any(
            el.get(a) is not None for a in ("data-series", "data-end", "data-role")
        ):
            continue
        if el.get("data-series") is None or el.get("data-end") is None:
            findings.append(
                f"label_binding_incomplete: {describe(el)}: a bound label requires data-series and data-end"
            )
            continue
        sname = el.get("data-series", "")
        end = el.get("data-end", "")
        role_attr = el.get("data-role")
        if end not in ("from", "to"):
            findings.append(
                f"label_end_unknown: {describe(el)}: data-end must be 'from' or 'to'"
            )
            continue
        if role_attr not in (None, "name", "value"):
            findings.append(
                f"label_role_unknown: {describe(el)}: data-role must be 'name', 'value' or absent"
            )
            continue
        role = "name" if role_attr == "name" else "value"
        if sname not in series:
            findings.append(
                f"label_series_unknown: {describe(el)}: no series line declares data-series='{sname}'"
            )
            continue
        labels.setdefault((sname, end, role), []).append(el)
        s = series[sname]
        visible = text_of(el)
        if role == "name":
            if visible != sname:
                findings.append(
                    f"name_mismatch: {describe(el)}: visible text {visible!r} != data-series {sname!r};"
                    " an unbound or swapped name renames the line"
                )
        else:
            bound = s["v_from"] if end == "from" else s["v_to"]
            tokens = NUM_TOKEN_RE.findall(visible)
            if not tokens:
                findings.append(
                    f"value_label_no_number: {describe(el)}: value label prints no number"
                )
            elif len(tokens) > 1:
                findings.append(
                    f"value_label_multiple_numbers: {describe(el)}: a value label must print exactly one"
                    f" complete number, found {len(tokens)} in {visible!r}"
                )
            else:
                value, err = token_value(tokens[0])
                if err is not None:
                    findings.append(f"value_label_bad_separator: {describe(el)}: {err}")
                elif bound is not None and value != bound:
                    findings.append(
                        f"value_mismatch: {describe(el)}: printed {value:g} != bound {bound:g}"
                        f" for series '{sname}' at the {end} end"
                    )
        lx = parse_float(el.get("x"))
        ly = parse_float(el.get("y"))
        if lx is None or ly is None:
            findings.append(
                f"label_position_unparsable: {describe(el)}: x/y must be numbers"
            )
            continue
        own = (s["x1"], s["y1"]) if end == "from" else (s["x2"], s["y2"])
        d_own = math.hypot(lx - own[0], ly - own[1])
        for other_name in order:
            if other_name == sname:
                continue
            o = series[other_name]
            for pt in ((o["x1"], o["y1"]), (o["x2"], o["y2"])):
                if math.hypot(lx - pt[0], ly - pt[1]) < d_own - 1e-9:
                    findings.append(
                        f"label_wrong_row: {describe(el)}: label at ({lx:g},{ly:g}) is nearer series"
                        f" '{other_name}' endpoint ({pt[0]:g},{pt[1]:g}) than its own"
                        f" ({own[0]:g},{own[1]:g}); a label on the wrong row renames the line"
                    )
                    break
            else:
                continue
            break

    for sname in order:
        for end in ("from", "to"):
            for role in ("name", "value"):
                got = labels.get((sname, end, role), [])
                if not got:
                    findings.append(
                        f"label_missing: <svg>: series '{sname}' has no {end}-end {role} label"
                    )
                elif len(got) > 1:
                    findings.append(
                        f"label_duplicate: {describe(got[-1])}: series '{sname}' has {len(got)}"
                        f" {end}-end {role} labels"
                    )

    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            a = series[order[i]]
            b = series[order[j]]
            dy_from = abs(a["y1"] - b["y1"])
            dy_to = abs(a["y2"] - b["y2"])
            if dy_from <= COINCIDE_TOL and dy_to <= COINCIDE_TOL:
                findings.append(
                    f"coincident_series: <svg>: '{order[i]}' and '{order[j]}' coincide at both"
                    " endpoints and cannot be separated; merge them or drop one and name the"
                    " omission in the source line"
                )
                continue
            for end, dy in (("from", dy_from), ("to", dy_to)):
                if dy < CROWD_PX:
                    findings.append(
                        f"endpoint_crowding: <svg>: '{order[i]}' and '{order[j]}' are {dy:g}px apart"
                        f" at the {end} end; crowded labels are data - merge or drop a series,"
                        " never move a point to open up space"
                    )

    findings.extend(transform_findings(root))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a slopegraph SVG against references/type-line.md."
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
