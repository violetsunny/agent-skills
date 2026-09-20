#!/usr/bin/env python3
"""Gate for the bump chart variant of the Line Chart type.

Contract source: references/type-line.md, section "Variants > Bump chart"
(honest-data rule, "Declaring the values", layout conventions).

Checks implemented:
- rank rows on the shipped grid y = 88 + 56 * (rank - 1), enforced with no
  tolerance at all ("there is no honest reason for a vertex to sit off its row")
- every snapshot's ranks must be a permutation of 1..N (a duplicated rank is
  a tie the stated tie-break cannot produce; a skipped rank is an empty row)
- every series must visit every snapshot: the shipped grammar has no way to
  declare a gap, so fewer vertices than columns is a finding
- data-series/data-ranks binding completeness; data-ranks is the basis of
  every geometric check, so a series whose labels go missing stays in the
  verified set and the missing label is itself reported
- M/L segment grammar (never splines), dots at every vertex (r=3, focal r=4),
  focus pairing (one accent hue carrying the unique heaviest stroke width)
- labels at first and last appearance, bound with data-series/data-end/
  data-role, checked on both axes: the row (series' rank row + 3.5) and the
  column (gutter x read off the figure - every label sharing an end and a
  role must agree on one column, outboard of the end it names)
- snapshot captions bound with data-axis/data-state exactly as the
  slopegraph binds its two
- series count 4-8, snapshots 3-6
- transform rejected on series paths, bound labels, ancestor <g> and CSS

Scope treaty: this gate reads data-ranks (its own vocabulary) and never reads
data-bins (the ridgeline's binding). A file with no data-ranks anywhere
belongs to a sibling gate: exit 0 with no findings and no mention of foreign
vocabulary, so neither gate claims the other's file.

Assumptions (the contract leaves these open):
- The row grid is pinned to the shipped constants (88, 56) with exact float
  equality; the gutter x is NOT pinned - it is read off the figure.
- Label rows sit at rank-row + 3.5 (the shipped convention, y=91.5 above
  row 88), tolerance 0.5px.
- Gutter columns: labels sharing (data-end, data-role) must agree on one x
  within 0.5px; first-end labels must sit left of the first snapshot column
  and last-end labels right of the last column (0.5px clearance).
- Snapshot columns are derived from the vertices of the series that visit
  every snapshot; captions index them 0-based via data-axis.
- Path grammar accepts absolute M/L only (the shipped open polyline,
  fill="none"); Z, relative commands and any curve command are findings.
- Dots are matched to vertices by position within 0.5px; unmatched circles
  (legend dots) are ignored; dot radius tolerance 0.01.
- Rank label text must be exactly "#<rank>" - the sigil keeps a rank from
  reading as a magnitude.
- The permutation check reads declared data-ranks even for a series missing
  vertices, so a truncated series reports visit_incomplete without silently
  shrinking the permutation.
- Any `transform` declaration inside <style> is rejected wholesale: CSS
  selectors are not resolved, because transforms are rejected rather than
  resolved.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB = (
    "data-series",
    "data-ranks",
    "data-end",
    "data-role",
    "data-axis",
    "data-state",
)
PATH_VOCAB = ("data-series", "data-ranks")
PATH_TOKEN_RE = re.compile(r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*[\d.]+)?\s*\)$"
)
HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")

ROW_Y0 = 88.0
ROW_PITCH = 56.0
LABEL_DY = 3.5
POINT_TOL = 0.5
DOT_TOL = 0.01
MIN_SERIES = 4
MAX_SERIES = 8
MIN_SNAPSHOTS = 3
MAX_SNAPSHOTS = 6
ENDS = ("first", "last")
ROLES = ("name", "rank")


def row_y(rank: int) -> float:
    return ROW_Y0 + ROW_PITCH * (rank - 1)


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


def parse_polyline_path(
    d: str | None,
) -> tuple[list[tuple[float, float]] | None, str | None]:
    """Parse the M ... L ... grammar (open, straight segments). Returns (vertices, error)."""
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
        else:
            return None, (
                f"command '{tok}' is outside the M/L segment grammar; a curve between two"
                " snapshots draws a trajectory nobody measured"
            )
    if cmds[0] != "M" or cmds.count("M") != 1:
        return None, "path must open with exactly one M command"
    return vertices, None


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
                " rendered mark away from the verified rank; bake the offset into the coordinates"
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


def focus_findings(items: list[dict]) -> list[str]:
    findings = []
    if not items:
        return findings
    max_w = max(it["width"] for it in items)
    focal_idx = [i for i, it in enumerate(items) if abs(it["width"] - max_w) < 1e-9]
    other_idx = [i for i in range(len(items)) if i not in focal_idx]
    if len(focal_idx) != 1:
        findings.append(
            f"focus_pairing: <svg>: exactly one series must carry the unique heaviest stroke"
            f" width; {len(focal_idx)} carry width {max_w:g}"
        )
    if other_idx:
        widths = [items[i]["width"] for i in other_idx]
        if max(widths) - min(widths) > DOT_TOL:
            findings.append(
                "focus_pairing: <svg>: non-focal series must share one common stroke width"
            )
        if len(focal_idx) == 1 and max_w <= max(widths) + 1e-9:
            findings.append(
                "focus_pairing: <svg>: the focal series' stroke width must exceed the common weight"
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
    return findings


def check(root: ET.Element) -> list[str]:
    findings: list[str] = []
    if not any(el.get("data-ranks") is not None for el in root.iter()):
        return findings

    series: dict[str, dict] = {}
    order: list[str] = []
    for el in root.iter():
        if local_name(el.tag) != "path":
            continue
        if not any(el.get(a) is not None for a in PATH_VOCAB):
            continue
        missing = [a for a in PATH_VOCAB if el.get(a) is None]
        if missing:
            findings.append(
                f"binding_path_incomplete: {describe(el)}: series path is missing {', '.join(missing)}"
            )
            continue
        name = el.get("data-series", "")
        if name in series:
            findings.append(
                f"duplicate_series: {describe(el)}: series '{name}' is declared twice"
            )
            continue
        record = {
            "el": el,
            "name": name,
            "ranks": None,
            "vertices": None,
            "width": parse_float(el.get("stroke-width")) or 1.0,
            "stroke_rgb": parse_color(el.get("stroke")),
        }
        series[name] = record
        order.append(name)

        ranks_raw = el.get("data-ranks", "")
        parts = [p.strip() for p in ranks_raw.split(",") if p.strip() != ""]
        ranks: list[int] = []
        bad = False
        for part in parts:
            if not re.match(r"^[-+]?\d+$", part):
                bad = True
                break
            ranks.append(int(part))
        if bad or not ranks:
            findings.append(
                f"ranks_unparsable: {describe(el)}: data-ranks must be a comma-separated list of integers"
            )
        else:
            record["ranks"] = ranks

        vertices, err = parse_polyline_path(el.get("d"))
        if err is not None:
            findings.append(f"segment_grammar: {describe(el)}: {err}")
        else:
            record["vertices"] = vertices

    n_series = len(series)
    if n_series and not MIN_SERIES <= n_series <= MAX_SERIES:
        findings.append(
            f"series_count: <svg>: {n_series} series declared; the bump chart contract requires"
            f" {MIN_SERIES}-{MAX_SERIES}"
        )

    visit_counts = [
        len(r["vertices"]) for r in series.values() if r["vertices"] is not None
    ]
    n_snap = max(visit_counts) if visit_counts else 0
    if n_snap and not MIN_SNAPSHOTS <= n_snap <= MAX_SNAPSHOTS:
        findings.append(
            f"snapshot_count: <svg>: {n_snap} snapshots; the bump chart contract requires"
            f" {MIN_SNAPSHOTS}-{MAX_SNAPSHOTS}"
        )

    for name in order:
        r = series[name]
        if r["vertices"] is None:
            continue
        if len(r["vertices"]) < n_snap:
            findings.append(
                f"visit_incomplete: {describe(r['el'])}: series '{name}' visits"
                f" {len(r['vertices'])} of {n_snap} snapshots; the grammar has no gap declaration,"
                " so a real gap must be a stated absence, never a truncated line"
            )
        if r["ranks"] is not None and len(r["ranks"]) != len(r["vertices"]):
            findings.append(
                f"ranks_length: {describe(r['el'])}: data-ranks declares {len(r['ranks'])} ranks for"
                f" {len(r['vertices'])} vertices"
            )

    col_x: list[float] = []
    ref_name = next(
        (
            nm
            for nm in order
            if series[nm]["vertices"] is not None
            and len(series[nm]["vertices"]) == n_snap
        ),
        None,
    )
    if ref_name is not None:
        col_x = [x for x, _ in series[ref_name]["vertices"]]
        for name in order:
            r = series[name]
            if (
                r["vertices"] is None
                or len(r["vertices"]) != n_snap
                or name == ref_name
            ):
                continue
            for i, (x, _) in enumerate(r["vertices"]):
                if abs(x - col_x[i]) > POINT_TOL:
                    findings.append(
                        f"column_x_mismatch: {describe(r['el'])}: vertex {i} at x={x:g} is off the"
                        f" shared snapshot column x={col_x[i]:g}"
                    )

    for name in order:
        r = series[name]
        if r["vertices"] is None or r["ranks"] is None:
            continue
        for i, ((x, y), rank) in enumerate(zip(r["vertices"], r["ranks"])):
            expected = row_y(rank)
            if y != expected:
                findings.append(
                    f"grid_row: {describe(r['el'])}: vertex {i} (rank {rank}) sits at y={y:g}, the grid"
                    f" says y={expected:g} with no tolerance; a vertex off its row reads as a rank"
                    " between two ranks"
                )

    for i in range(n_snap):
        column_ranks = [
            series[nm]["ranks"][i]
            for nm in order
            if series[nm]["ranks"] is not None and len(series[nm]["ranks"]) > i
        ]
        if sorted(column_ranks) != list(range(1, n_series + 1)):
            where = f"x={col_x[i]:g}" if i < len(col_x) else f"index {i}"
            findings.append(
                f"rank_permutation: <svg>: snapshot {i} ({where}) ranks {sorted(column_ranks)} are not a"
                f" permutation of 1..{n_series}; a duplicated rank is a tie the stated tie-break"
                " cannot produce and a skipped rank is an empty row"
            )

    circles = []
    for el in root.iter():
        if local_name(el.tag) != "circle":
            continue
        cx = parse_float(el.get("cx"))
        cy = parse_float(el.get("cy"))
        cr = parse_float(el.get("r"))
        if cx is not None and cy is not None:
            circles.append({"el": el, "cx": cx, "cy": cy, "r": cr})

    focus_items = [series[nm] for nm in order]
    findings.extend(focus_findings(focus_items))
    max_w = max((it["width"] for it in focus_items), default=0.0)
    focal_names = {it["name"] for it in focus_items if abs(it["width"] - max_w) < 1e-9}

    for name in order:
        r = series[name]
        if r["vertices"] is None:
            continue
        expected_r = 4.0 if name in focal_names else 3.0
        for i, (x, y) in enumerate(r["vertices"]):
            matched = [
                c
                for c in circles
                if abs(c["cx"] - x) <= POINT_TOL and abs(c["cy"] - y) <= POINT_TOL
            ]
            if not matched:
                findings.append(
                    f"dot_missing: {describe(r['el'])}: no dot at vertex {i} ({x:g},{y:g}); every"
                    " vertex carries a dot"
                )
                continue
            dot = matched[0]
            if dot["r"] is None:
                findings.append(
                    f"dot_radius: {describe(dot['el'])}: dot at vertex {i} of '{name}' has no parsable r"
                )
            elif abs(dot["r"] - expected_r) > DOT_TOL:
                findings.append(
                    f"dot_radius: {describe(dot['el'])}: dot at vertex {i} of '{name}' has r={dot['r']:g},"
                    f" expected {expected_r:g} (focal r=4, others r=3)"
                )

    labels: dict[tuple[str, str, str], list[ET.Element]] = {}
    label_groups: dict[tuple[str, str], list[tuple[ET.Element, float]]] = {}
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        if el.get("data-axis") is not None or el.get("data-state") is not None:
            continue
        if not any(
            el.get(a) is not None for a in ("data-series", "data-end", "data-role")
        ):
            continue
        if (
            el.get("data-series") is None
            or el.get("data-end") is None
            or el.get("data-role") is None
        ):
            findings.append(
                f"label_binding_incomplete: {describe(el)}: a bound label requires data-series,"
                " data-end and data-role"
            )
            continue
        sname = el.get("data-series", "")
        end = el.get("data-end", "")
        role = el.get("data-role", "")
        if end not in ENDS:
            findings.append(
                f"label_end_unknown: {describe(el)}: data-end must be 'first' or 'last'"
            )
            continue
        if role not in ROLES:
            findings.append(
                f"label_role_unknown: {describe(el)}: data-role must be 'name' or 'rank'"
            )
            continue
        if sname not in series:
            findings.append(
                f"label_series_unknown: {describe(el)}: no series path declares data-series='{sname}'"
            )
            continue
        labels.setdefault((sname, end, role), []).append(el)
        r = series[sname]
        ranks = r["ranks"]
        rank_at_end = None
        if ranks:
            rank_at_end = ranks[0] if end == "first" else ranks[-1]
        visible = text_of(el)
        if role == "name":
            if visible != sname:
                findings.append(
                    f"name_mismatch: {describe(el)}: visible text {visible!r} != data-series {sname!r}"
                )
        elif rank_at_end is not None and visible != f"#{rank_at_end}":
            findings.append(
                f"rank_mismatch: {describe(el)}: printed {visible!r} != bound rank #{rank_at_end}"
                f" for series '{sname}' at the {end} snapshot"
            )
        lx = parse_float(el.get("x"))
        ly = parse_float(el.get("y"))
        if lx is None or ly is None:
            findings.append(
                f"label_position_unparsable: {describe(el)}: x/y must be numbers"
            )
        else:
            if (
                rank_at_end is not None
                and abs(ly - (row_y(rank_at_end) + LABEL_DY)) > POINT_TOL
            ):
                findings.append(
                    f"label_off_row: {describe(el)}: label y={ly:g} is not on its series' row"
                    f" (rank {rank_at_end} row {row_y(rank_at_end):g} + {LABEL_DY:g}); the row says"
                    " which series a label belongs to"
                )
            if col_x:
                if end == "first" and lx >= col_x[0] - POINT_TOL:
                    findings.append(
                        f"gutter_side: {describe(el)}: first-end label at x={lx:g} is not in the gutter"
                        f" outboard of the first snapshot column (x < {col_x[0]:g}); the column says"
                        " which end a label names"
                    )
                if end == "last" and lx <= col_x[-1] + POINT_TOL:
                    findings.append(
                        f"gutter_side: {describe(el)}: last-end label at x={lx:g} is not in the gutter"
                        f" outboard of the last snapshot column (x > {col_x[-1]:g})"
                    )
            label_groups.setdefault((end, role), []).append((el, lx))

    for name in order:
        for end in ENDS:
            for role in ROLES:
                got = labels.get((name, end, role), [])
                if not got:
                    findings.append(
                        f"label_missing: <svg>: series '{name}' has no {end}-end {role} label"
                    )
                elif len(got) > 1:
                    findings.append(
                        f"label_duplicate: {describe(got[-1])}: series '{name}' has {len(got)}"
                        f" {end}-end {role} labels"
                    )

    for (end, role), members in sorted(label_groups.items()):
        xs = [lx for _, lx in members if lx is not None]
        if len(xs) >= 2 and max(xs) - min(xs) > POINT_TOL:
            offenders = ", ".join(
                describe(el)
                for el, lx in members
                if lx is not None and abs(lx - sorted(xs)[len(xs) // 2]) > POINT_TOL
            )
            findings.append(
                f"gutter_column: <svg>: {end}-end {role} labels disagree on one column"
                f" (x values {', '.join(f'{x:g}' for x in sorted(set(xs)))}); offenders: {offenders}"
            )

    captions: dict[int, list[ET.Element]] = {}
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        has_axis = el.get("data-axis") is not None
        has_state = el.get("data-state") is not None
        if not (has_axis or has_state):
            continue
        if not (has_axis and has_state):
            findings.append(
                f"caption_binding: {describe(el)}: a snapshot caption requires both data-axis and data-state"
            )
            continue
        raw_axis = el.get("data-axis", "")
        if not re.match(r"^\d+$", raw_axis.strip()):
            findings.append(
                f"caption_axis: {describe(el)}: data-axis must be a 0-based snapshot index, got {raw_axis!r}"
            )
            continue
        idx = int(raw_axis.strip())
        if n_snap and not 0 <= idx < n_snap:
            findings.append(
                f"caption_axis: {describe(el)}: data-axis={idx} is outside the {n_snap} snapshots"
            )
            continue
        state = el.get("data-state", "")
        if text_of(el) != state:
            findings.append(
                f"caption_text_mismatch: {describe(el)}: visible text {text_of(el)!r} != data-state {state!r}"
            )
        cx = parse_float(el.get("x"))
        if (
            col_x
            and cx is not None
            and idx < len(col_x)
            and abs(cx - col_x[idx]) > POINT_TOL
        ):
            findings.append(
                f"caption_position: {describe(el)}: caption x={cx:g} is not on snapshot column"
                f" {idx} (x={col_x[idx]:g})"
            )
        captions.setdefault(idx, []).append(el)
    for i in range(n_snap):
        got = captions.get(i, [])
        if not got:
            findings.append(
                f"caption_missing: <svg>: no caption is bound with data-axis='{i}'"
            )
        elif len(got) > 1:
            findings.append(
                f"caption_duplicate: {describe(got[-1])}: {len(got)} captions are bound with data-axis='{i}'"
            )

    findings.extend(transform_findings(root))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a bump chart SVG against references/type-line.md."
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
