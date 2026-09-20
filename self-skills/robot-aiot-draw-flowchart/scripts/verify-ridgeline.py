#!/usr/bin/env python3
"""Gate for the ridgeline variant of the Line Chart type.

Contract source: references/type-line.md, section "Variants > Ridgeline"
(honest-data rule, "Declaring the values", anti-patterns).

Checks implemented:
- one amplitude for the whole figure, derived from the figure itself and
  enforced on every vertex of every ridge (per-ridge normalisation or any
  second amplitude anywhere is a finding)
- baselines on one fixed pitch; ridge count 3-12; bins 8-40 and shared
  across ridges
- data-ridge/data-bins/data-baseline binding completeness on outlines,
  baseline rules (data-role="baseline") and labels (data-role name/range)
- M/L/Z segment grammar; vertices on one shared evenly spaced bin grid;
  first and last bin zero (no cliff); outline closed on its own baseline
- overlap ceiling: no peak may reach the row two above (height <= pitch)
- focus pairing: exactly one focal ridge carrying both the unique heaviest
  stroke width and the single accent hue; the ink ramp shares one hue; fill
  hue matches stroke hue
- every label bound and cross-checked; the printed range is verified against
  the first and last nonzero bin through the figure's own tick scale
  (data-tick/data-bin)
- transform rejected on outlines, baseline rules, bound labels, ancestor <g>
  and CSS

Scope treaty: this gate reads data-bins (its own vocabulary) and never reads
data-series (the slopegraph's binding). A file with no data-bins anywhere
belongs to a sibling gate: exit 0 with no findings and no mention of foreign
vocabulary, so neither gate claims the other's file.

Assumptions (the contract leaves these open):
- The amplitude is pixels per bin unit, derived by least squares through the
  origin over every (bin, baseline - y) pair with bin > 0; the per-vertex
  residual tolerance is 0.5px.
- Pitch tolerance is 0.5px; the overlap ceiling is height <= pitch + 0.5px.
- The path grammar accepts absolute M/L/Z only (the shipped grammar);
  relative commands and any curve command are findings.
- The tick scale is a least-squares line over (x, data-bin); tick text must
  equal its data-bin exactly; tick residual and printed-range tolerances are
  2px expressed in value units (|m| * 2). Fewer than two usable ticks means
  the x-scale is not printed: xscale_unprinted, and range cross-checks are
  skipped.
- Label rows sit at baseline + 3.5 (the shipped convention), tolerance
  0.5px; name labels sit left of the bin run, range labels right of it.
- Any `transform` declaration inside <style> is rejected wholesale: CSS
  selectors are not resolved, because transforms are rejected rather than
  resolved. The rotated amplitude caption stays legal because it carries no
  binding attributes.
- Baseline rules and geometry are compared against the run of the first
  ridge with parsable vertices; that run is the figure's shared bin grid.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = (
    "data-ridge",
    "data-bins",
    "data-baseline",
    "data-role",
    "data-tick",
    "data-bin",
)
OUTLINE_VOCAB = ("data-ridge", "data-bins", "data-baseline")
NUM_TOKEN_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
CANONICAL_COMMA_RE = re.compile(r"^[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
PATH_TOKEN_RE = re.compile(r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*[\d.]+)?\s*\)$"
)
HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")

POINT_TOL = 0.5
PITCH_TOL = 0.5
LABEL_DY = 3.5
MIN_RIDGES = 3
MAX_RIDGES = 12
MIN_BINS = 8
MAX_BINS = 40


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


def parse_straight_path(
    d: str | None,
) -> tuple[list[tuple[float, float]] | None, str | None]:
    """Parse the M ... L ... Z segment grammar. Returns (vertices, error)."""
    if d is None:
        return None, "path has no d attribute"
    leftover = PATH_TOKEN_RE.sub("", d)
    if leftover.strip(" ,\t\n\r"):
        return (
            None,
            f"path data contains unparsable characters {leftover.strip()[:20]!r}",
        )
    tokens = PATH_TOKEN_RE.findall(d)
    if not tokens:
        return None, "path data is empty"
    vertices: list[tuple[float, float]] = []
    cmds: list[str] = []
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if tok in ("M", "L"):
            cmds.append(tok)
            coords: list[str] = []
            i += 1
            while i < n and not tokens[i].isalpha():
                coords.append(tokens[i])
                i += 1
            if len(coords) < 2 or len(coords) % 2 != 0:
                return None, f"{tok} command has malformed coordinate pairs"
            for j in range(0, len(coords), 2):
                vertices.append((float(coords[j]), float(coords[j + 1])))
        elif tok == "Z":
            cmds.append("Z")
            i += 1
        else:
            return (
                None,
                f"command '{tok}' is outside the M/L/Z segment grammar (no splines, no relative commands)",
            )
    if cmds[0] != "M" or cmds.count("M") != 1:
        return None, "path must open with exactly one M command"
    if cmds[-1] != "Z" or cmds.count("Z") != 1:
        return None, "path must be closed with exactly one trailing Z"
    return vertices, None


def fit_line(points: list[tuple[float, float]]) -> tuple[float, float] | None:
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


def token_value(token: str) -> tuple[float | None, str | None]:
    if "," in token:
        if not CANONICAL_COMMA_RE.match(token):
            return None, f"thousands separator in {token!r} is not canonical grouping"
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
                " rendered mark away from the verified bin; bake the offset into the coordinates"
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


def focus_findings(items: list[dict], kind: str) -> list[str]:
    findings = []
    if not items:
        return findings
    max_w = max(it["width"] for it in items)
    focal_idx = [i for i, it in enumerate(items) if abs(it["width"] - max_w) < 1e-9]
    other_idx = [i for i in range(len(items)) if i not in focal_idx]
    if len(focal_idx) != 1:
        findings.append(
            f"focus_pairing: <svg>: exactly one {kind} must carry the unique heaviest stroke"
            f" width; {len(focal_idx)} carry width {max_w:g}"
        )
    if other_idx:
        widths = [items[i]["width"] for i in other_idx]
        if max(widths) - min(widths) > 0.01:
            findings.append(
                f"focus_pairing: <svg>: non-focal {kind}s must share one common stroke width"
            )
        if len(focal_idx) == 1 and max_w <= max(widths) + 1e-9:
            findings.append(
                f"focus_pairing: <svg>: the focal {kind}'s stroke width must exceed the common weight"
            )
    hues: dict[tuple, list[str]] = {}
    for i in other_idx:
        rgb = items[i]["stroke_rgb"]
        if rgb is not None:
            hues.setdefault(rgb, []).append(items[i]["name"])
    ink_rgb = None
    if len(hues) > 1:
        findings.append(
            f"ink_ramp_mismatch: <svg>: non-focal strokes must share one ink hue, found {len(hues)}"
        )
    elif len(hues) == 1:
        ink_rgb = next(iter(hues))
    for i in focal_idx:
        rgb = items[i]["stroke_rgb"]
        if rgb is not None and ink_rgb is not None and rgb == ink_rgb:
            findings.append(
                f"focus_pairing: {describe(items[i]['el'])}: the focal stroke must be the single"
                " accent, not a member of the ink ramp"
            )
    for it in items:
        if (
            it.get("fill_rgb") is not None
            and it["stroke_rgb"] is not None
            and it["fill_rgb"] != it["stroke_rgb"]
        ):
            findings.append(
                f"fill_hue_mismatch: {describe(it['el'])}: fill hue must match the stroke hue"
                " (accent fill on the focal ridge, ink fill on the rest)"
            )
    return findings


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    if not any(el.get("data-bins") is not None for el in root.iter()):
        return findings

    ridges: dict[str, dict] = {}
    order: list[str] = []
    for el in root.iter():
        if local_name(el.tag) != "path":
            continue
        if not any(el.get(a) is not None for a in OUTLINE_VOCAB):
            continue
        missing = [a for a in OUTLINE_VOCAB if el.get(a) is None]
        if missing:
            findings.append(
                f"binding_path_incomplete: {describe(el)}: ridge outline is missing {', '.join(missing)}"
            )
            continue
        rid = el.get("data-ridge", "")
        if rid in ridges:
            findings.append(
                f"duplicate_ridge: {describe(el)}: ridge '{rid}' is declared twice"
            )
            continue
        record = {
            "el": el,
            "name": rid,
            "bins": None,
            "baseline": None,
            "vertices": None,
        }
        ridges[rid] = record
        order.append(rid)

        bins_raw = el.get("data-bins", "")
        parts = [p.strip() for p in bins_raw.split(",") if p.strip() != ""]
        bins: list[float] = []
        bad = False
        for part in parts:
            if not re.match(r"^[-+]?\d+(?:\.\d+)?$", part):
                bad = True
                break
            bins.append(float(part))
        if bad or not bins:
            findings.append(
                f"bins_unparsable: {describe(el)}: data-bins must be a comma-separated list of numbers"
            )
        else:
            record["bins"] = bins

        baseline = parse_float(el.get("data-baseline"))
        if baseline is None:
            findings.append(
                f"binding_value_unparsable: {describe(el)}: data-baseline must be a number"
            )
        else:
            record["baseline"] = baseline

        vertices, err = parse_straight_path(el.get("d"))
        if err is not None:
            findings.append(f"segment_grammar: {describe(el)}: {err}")
        else:
            record["vertices"] = vertices

        record["width"] = parse_float(el.get("stroke-width")) or 1.0
        record["stroke_rgb"] = parse_color(el.get("stroke"))
        fill = el.get("fill")
        record["fill_rgb"] = None if fill in (None, "none") else parse_color(fill)

    count = len(ridges)
    if count and not MIN_RIDGES <= count <= MAX_RIDGES:
        findings.append(
            f"ridge_count: <svg>: {count} ridges declared; the ridgeline contract requires"
            f" {MIN_RIDGES}-{MAX_RIDGES}"
        )

    ref_bin_count = None
    run: dict | None = None
    for rid in order:
        r = ridges[rid]
        bins = r["bins"]
        vertices = r["vertices"]
        if bins is None:
            continue
        if not MIN_BINS <= len(bins) <= MAX_BINS:
            findings.append(
                f"bin_count: {describe(r['el'])}: {len(bins)} bins; the contract requires {MIN_BINS}-{MAX_BINS}"
            )
        if ref_bin_count is None:
            ref_bin_count = len(bins)
        elif len(bins) != ref_bin_count:
            findings.append(
                f"bin_count_mismatch: {describe(r['el'])}: {len(bins)} bins vs {ref_bin_count} on the"
                " first ridge; every ridge shares one x-scale and one sampling"
            )
        if vertices is not None and len(vertices) != len(bins):
            findings.append(
                f"segment_grammar: {describe(r['el'])}: {len(vertices)} vertices for {len(bins)} bins;"
                " data-bins is the basis of every geometric check"
            )
        if bins[0] != 0:
            findings.append(
                f"ridge_cliff: {describe(r['el'])}: first bin is {bins[0]:g}, not 0; a ridge starts on"
                " its own baseline or the outline closes as a cliff"
            )
        if bins[-1] != 0:
            findings.append(
                f"ridge_cliff: {describe(r['el'])}: last bin is {bins[-1]:g}, not 0; a ridge ends on"
                " its own baseline or the outline closes as a cliff"
            )
        if vertices is not None:
            n = len(vertices)
            x0 = vertices[0][0]
            xlast = vertices[-1][0]
            if n >= 2:
                step = (xlast - x0) / (n - 1)
                for i, (x, _) in enumerate(vertices):
                    if abs(x - (x0 + i * step)) > POINT_TOL:
                        findings.append(
                            f"x_grid_uneven: {describe(r['el'])}: vertex {i} at x={x:g} is off the evenly"
                            f" spaced bin grid (expected {x0 + i * step:g})"
                        )
                        break
            if run is None:
                run = {"x0": x0, "xlast": xlast, "xs": [v[0] for v in vertices]}
            elif (
                abs(x0 - run["x0"]) > POINT_TOL or abs(xlast - run["xlast"]) > POINT_TOL
            ):
                findings.append(
                    f"x_range_mismatch: {describe(r['el'])}: ridge runs x={x0:g}..{xlast:g} vs the shared"
                    f" run x={run['x0']:g}..{run['xlast']:g}; every ridge shares one x-scale"
                )
            if r["baseline"] is not None:
                if abs(vertices[0][1] - r["baseline"]) > POINT_TOL:
                    findings.append(
                        f"ridge_not_closed_on_baseline: {describe(r['el'])}: first vertex y={vertices[0][1]:g}"
                        f" is not on the declared baseline {r['baseline']:g}"
                    )
                if abs(vertices[-1][1] - r["baseline"]) > POINT_TOL:
                    findings.append(
                        f"ridge_not_closed_on_baseline: {describe(r['el'])}: last vertex y={vertices[-1][1]:g}"
                        f" is not on the declared baseline {r['baseline']:g}"
                    )

    amp_points: list[tuple[float, float]] = []
    for rid in order:
        r = ridges[rid]
        if r["bins"] is None or r["vertices"] is None or r["baseline"] is None:
            continue
        if len(r["vertices"]) != len(r["bins"]):
            continue
        for b, (_, y) in zip(r["bins"], r["vertices"]):
            if b > 0:
                amp_points.append((b, r["baseline"] - y))
    amplitude = None
    sbb = sum(b * b for b, _ in amp_points)
    if sbb <= 1e-12:
        if ridges:
            findings.append(
                "amplitude_underivable: <svg>: no nonzero bin mass anywhere; the figure's single"
                " amplitude cannot be derived"
            )
    else:
        amplitude = sum(b * h for b, h in amp_points) / sbb
        for rid in order:
            r = ridges[rid]
            if r["bins"] is None or r["vertices"] is None or r["baseline"] is None:
                continue
            if len(r["vertices"]) != len(r["bins"]):
                continue
            for i, (b, (_, y)) in enumerate(zip(r["bins"], r["vertices"])):
                h = r["baseline"] - y
                if abs(h - amplitude * b) > POINT_TOL:
                    findings.append(
                        f"amplitude_violation: {describe(r['el'])}: vertex {i} (bin {b:g}) rises {h:g}px,"
                        f" the figure's single amplitude says {amplitude * b:.3f}px; per-ridge"
                        " normalisation destroys the comparison the type exists for"
                    )

    baselines = sorted(
        r["baseline"] for r in ridges.values() if r["baseline"] is not None
    )
    pitch = None
    if len(baselines) >= 2:
        diffs = [b2 - b1 for b1, b2 in zip(baselines, baselines[1:])]
        if max(diffs) - min(diffs) > PITCH_TOL:
            findings.append(
                f"pitch_uneven: <svg>: baselines {', '.join(f'{b:g}' for b in baselines)} are not on a"
                " fixed pitch; a baseline nudged off the row is the same falsification as a private"
                " amplitude"
            )
        pitch = sum(diffs) / len(diffs)

    heights: list[float] = []
    for r in ridges.values():
        if r["vertices"] and r["baseline"] is not None:
            heights.extend(r["baseline"] - y for _, y in r["vertices"])
    max_height = max(heights) if heights else 0.0
    if pitch is not None and max_height > pitch + POINT_TOL:
        findings.append(
            f"overlap_ceiling: <svg>: tallest ridge rises {max_height:g}px against a pitch of"
            f" {pitch:g}px; a peak reaching the row two above is occluded - more pitch, never a"
            " smaller amplitude on one ridge"
        )

    rules: dict[str, list[ET.Element]] = {}
    for el in root.iter():
        if local_name(el.tag) != "line":
            continue
        has_ridge = el.get("data-ridge") is not None
        has_role = el.get("data-role") is not None
        if not (has_ridge or has_role):
            continue
        if not (has_ridge and el.get("data-role") == "baseline"):
            findings.append(
                f"baseline_rule_binding: {describe(el)}: a baseline rule requires data-ridge and"
                ' data-role="baseline"'
            )
            continue
        rules.setdefault(el.get("data-ridge", ""), []).append(el)
    for rid in order:
        got = rules.get(rid, [])
        if not got:
            findings.append(
                f"baseline_rule_missing: <svg>: ridge '{rid}' has no baseline rule"
            )
            continue
        if len(got) > 1:
            findings.append(
                f"baseline_rule_duplicate: {describe(got[-1])}: ridge '{rid}' has {len(got)} baseline rules"
            )
        r = ridges[rid]
        for el in got:
            y1 = parse_float(el.get("y1"))
            y2 = parse_float(el.get("y2"))
            x1 = parse_float(el.get("x1"))
            x2 = parse_float(el.get("x2"))
            if None in (y1, y2, x1, x2):
                findings.append(
                    f"geometry_unparsable: {describe(el)}: baseline rule coordinates must be numbers"
                )
                continue
            if abs(y1 - y2) > 0.01:
                findings.append(
                    f"baseline_rule_not_horizontal: {describe(el)}: baseline rule is not horizontal"
                )
            if r["baseline"] is not None and abs(y1 - r["baseline"]) > POINT_TOL:
                findings.append(
                    f"baseline_rule_mismatch: {describe(el)}: rule drawn at y={y1:g} but ridge '{rid}'"
                    f" declares data-baseline={r['baseline']:g}"
                )
            if run is not None and (
                abs(x1 - run["x0"]) > POINT_TOL or abs(x2 - run["xlast"]) > POINT_TOL
            ):
                findings.append(
                    f"baseline_rule_span: {describe(el)}: rule spans x={x1:g}..{x2:g}, not the full bin"
                    f" run x={run['x0']:g}..{run['xlast']:g}"
                )

    findings.extend(focus_findings([ridges[rid] for rid in order], "ridge"))

    labels: dict[tuple[str, str], list[ET.Element]] = {}
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        has_ridge = el.get("data-ridge") is not None
        has_role = el.get("data-role") is not None
        if not (has_ridge or has_role):
            continue
        if not (has_ridge and has_role):
            findings.append(
                f"label_binding_incomplete: {describe(el)}: a bound label requires data-ridge and data-role"
            )
            continue
        rid = el.get("data-ridge", "")
        role = el.get("data-role", "")
        if role not in ("name", "range"):
            findings.append(
                f"label_role_unknown: {describe(el)}: data-role must be 'name' or 'range'"
            )
            continue
        if rid not in ridges:
            findings.append(
                f"label_ridge_unknown: {describe(el)}: no ridge outline declares data-ridge='{rid}'"
            )
            continue
        labels.setdefault((rid, role), []).append(el)
        r = ridges[rid]
        lx = parse_float(el.get("x"))
        ly = parse_float(el.get("y"))
        if lx is None or ly is None:
            findings.append(
                f"label_position_unparsable: {describe(el)}: x/y must be numbers"
            )
        else:
            if (
                r["baseline"] is not None
                and abs(ly - (r["baseline"] + LABEL_DY)) > POINT_TOL
            ):
                findings.append(
                    f"label_off_row: {describe(el)}: label y={ly:g} is not on its ridge's row"
                    f" (baseline {r['baseline']:g} + {LABEL_DY:g})"
                )
            if run is not None:
                if role == "name" and lx >= run["x0"] - POINT_TOL:
                    findings.append(
                        f"label_side: {describe(el)}: name label at x={lx:g} must sit left of the bin run"
                        f" (x < {run['x0']:g})"
                    )
                if role == "range" and lx <= run["xlast"] + POINT_TOL:
                    findings.append(
                        f"label_side: {describe(el)}: range label at x={lx:g} must sit right of the bin"
                        f" run (x > {run['xlast']:g})"
                    )
        if role == "name":
            visible = text_of(el)
            if visible != rid:
                findings.append(
                    f"name_mismatch: {describe(el)}: visible text {visible!r} != data-ridge {rid!r}"
                )

    for rid in order:
        for role in ("name", "range"):
            got = labels.get((rid, role), [])
            if not got:
                findings.append(
                    f"label_missing: <svg>: ridge '{rid}' has no {role} label"
                )
            elif len(got) > 1:
                findings.append(
                    f"label_duplicate: {describe(got[-1])}: ridge '{rid}' has {len(got)} {role} labels"
                )

    ticks: list[dict] = []
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        has_tick = el.get("data-tick") is not None
        has_bin = el.get("data-bin") is not None
        if not (has_tick or has_bin):
            continue
        if not (has_tick and has_bin):
            findings.append(
                f"tick_binding: {describe(el)}: a bin tick requires both data-tick and data-bin"
            )
            continue
        value = parse_float(el.get("data-bin"))
        if value is None:
            findings.append(
                f"tick_value_unparsable: {describe(el)}: data-bin must be a number"
            )
            continue
        visible = text_of(el)
        tokens = NUM_TOKEN_RE.findall(visible)
        if len(tokens) != 1:
            findings.append(
                f"tick_text_mismatch: {describe(el)}: tick must print exactly one complete number,"
                f" found {len(tokens)} in {visible!r}"
            )
        else:
            printed, err = token_value(tokens[0])
            if err is not None:
                findings.append(f"tick_text_mismatch: {describe(el)}: {err}")
            elif printed != value:
                findings.append(
                    f"tick_text_mismatch: {describe(el)}: printed {printed:g} != data-bin {value:g}"
                )
        tx = parse_float(el.get("x"))
        if tx is None:
            findings.append(
                f"label_position_unparsable: {describe(el)}: x must be a number"
            )
        else:
            if run is not None and min(abs(tx - gx) for gx in run["xs"]) > POINT_TOL:
                findings.append(
                    f"tick_off_bin: {describe(el)}: tick x={tx:g} is not centred on a bin position"
                )
            ticks.append({"el": el, "x": tx, "value": value})

    scale = None
    if len(ticks) < 2:
        findings.append(
            "xscale_unprinted: <svg>: fewer than two bound bin ticks; the shared x-scale is not"
            " printed, so ranges cannot be cross-checked"
        )
    else:
        fit = fit_line([(t["x"], t["value"]) for t in ticks])
        if fit is None:
            findings.append(
                "xscale_unprinted: <svg>: bin ticks do not establish a linear x-scale (all ticks at one x?)"
            )
        else:
            c, m = fit
            tol = abs(m) * 2.0 + 1e-9
            for t in ticks:
                if abs(t["value"] - (c + m * t["x"])) > tol:
                    findings.append(
                        f"tick_scale_inconsistent: {describe(t['el'])}: data-bin {t['value']:g} at x={t['x']:g}"
                        f" is off the tick scale ({c + m * t['x']:.3f}); the ticks must print one linear x-scale"
                    )
            scale = (c, m, tol)

    if scale is not None and run is not None:
        c, m, tol = scale
        for rid in order:
            r = ridges[rid]
            if r["bins"] is None or r["vertices"] is None:
                continue
            if len(r["vertices"]) != len(r["bins"]):
                continue
            nonzero = [i for i, b in enumerate(r["bins"]) if b != 0]
            for el in labels.get((rid, "range"), []):
                if not nonzero:
                    continue
                visible = text_of(el)
                tokens = NUM_TOKEN_RE.findall(visible)
                if len(tokens) != 2:
                    findings.append(
                        f"range_format: {describe(el)}: range label must print exactly two numbers"
                        f" (first-last nonzero bin), found {len(tokens)} in {visible!r}"
                    )
                    continue
                values = []
                bad = False
                for token in tokens:
                    v, err = token_value(token)
                    if err is not None:
                        findings.append(f"range_format: {describe(el)}: {err}")
                        bad = True
                        break
                    values.append(v)
                if bad:
                    continue
                xf = r["vertices"][nonzero[0]][0]
                xl = r["vertices"][nonzero[-1]][0]
                expected_first = c + m * xf
                expected_last = c + m * xl
                if (
                    abs(values[0] - expected_first) > tol
                    or abs(values[1] - expected_last) > tol
                ):
                    findings.append(
                        f"range_mismatch: {describe(el)}: printed range {values[0]:g}-{values[1]:g} disagrees"
                        f" with the first/last nonzero bin through the figure's own tick scale"
                        f" ({expected_first:.3f}-{expected_last:.3f}); a range widened by a word is a finding"
                    )

    findings.extend(transform_findings(root))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a ridgeline SVG against references/type-line.md."
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
