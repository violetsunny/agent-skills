#!/usr/bin/env python3
"""Both-polarity tests for verify-bump.py.

Contract source: references/type-line.md, section "Variants > Bump chart":
"scripts/test-verify-bump.py proves each check in both polarities."

Every check gets a passing polarity and a violating polarity. The passing
polarity for all checks at once is the base fixture (a complete, honest
four-series three-snapshot figure that must exit 0 with no output); targeted
passing variants prove the exemptions (rotated unbound decoration,
out-of-scope file). Each violating fixture is the base figure with exactly
one deliberate defect, built from parameters rather than string surgery so
geometry stays self-consistent. A violation case asserts exit code 1 and
that the target rule fires; incidental findings caused by the same defect
are tolerated.

The scope treaty case pins that this gate never reads data-bins: a file
speaking only the ridgeline's vocabulary exits 0 with no findings - the gate
does not claim the other's file.

Fixtures are synthetic SVG strings; no external files are read.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-bump.py"

ROW_Y0 = 88
ROW_PITCH = 56
BASE_COL_X = [320, 440, 560]
BASE_SERIES = [
    ("alpha", [1, 2, 3], True),
    ("beta", [2, 1, 4], False),
    ("gamma", [3, 4, 1], False),
    ("delta", [4, 3, 2], False),
]
BASE_CAPTIONS = [(0, "Q1"), (1, "Q2"), (2, "Q3")]
INK_ALPHAS = ("0.8", "0.71", "0.62", "0.66", "0.75")

RIDGE_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<path data-ridge="checkout-api" data-baseline="320" data-bins="0,1,6,17,21,14,8,6,7,9,7,4,0" d="M320,320 L350,317.6 L380,305.6 L410,279.2 L440,269.6 L470,286.4 L500,300.8 L530,305.6 L560,303.2 L590,298.4 L620,303.2 L650,310.4 L680,320 Z" fill="rgba(235,108,54,0.16)" stroke="#eb6c36" stroke-width="2.4"/>
<text data-ridge="checkout-api" data-role="name" x="304" y="323.5" text-anchor="end">checkout-api</text>
<text data-ridge="checkout-api" data-role="range" x="696" y="323.5">40\u2013440 ms</text>
</svg>
"""


def row_y(rank: int) -> float:
    return ROW_Y0 + ROW_PITCH * (rank - 1)


def fmt(value: float) -> str:
    rounded = round(value, 6)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:g}"


def build(
    series=None,
    col_x=None,
    captions=None,
    widths=None,
    strokes=None,
    ranks_attr=None,
    d_override=None,
    path_transform=None,
    dot_drop=(),
    dot_r=None,
    label_texts=None,
    label_x=None,
    label_dy=None,
    label_end=None,
    caption_x=None,
    caption_texts=None,
    caption_axis=None,
    drop=(),
    group_transform=None,
    style=None,
    extra_svg="",
):
    series = BASE_SERIES if series is None else series
    col_x = BASE_COL_X if col_x is None else col_x
    captions = BASE_CAPTIONS if captions is None else captions
    widths = widths or {}
    strokes = strokes or {}
    ranks_attr = ranks_attr or {}
    d_override = d_override or {}
    path_transform = path_transform or {}
    dot_drop = set(dot_drop)
    dot_r = dot_r or {}
    label_texts = label_texts or {}
    label_x = label_x or {}
    label_dy = label_dy or {}
    label_end = label_end or {}
    caption_x = caption_x or {}
    caption_texts = caption_texts or {}
    caption_axis = caption_axis or {}
    drop = set(drop)

    gutter = {
        ("first", "name"): col_x[0] - 48,
        ("first", "rank"): col_x[0] - 16,
        ("last", "rank"): col_x[-1] + 16,
        ("last", "name"): col_x[-1] + 48,
    }

    parts = []
    if style:
        parts.append(f"<style>{style}</style>")
    if group_transform is not None:
        parts.append(f'<g transform="{group_transform}">')

    nonfocal = 0
    for name, ranks, focal in series:
        vertices = [(col_x[i], row_y(r)) for i, r in enumerate(ranks)]
        d = d_override.get(name) or (
            "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in vertices)
        )
        ranks_str = ranks_attr.get(name) or ",".join(str(r) for r in ranks)
        if focal:
            stroke = strokes.get(name, "#eb6c36")
            width = widths.get(name, "2.4")
        else:
            alpha = INK_ALPHAS[nonfocal % len(INK_ALPHAS)]
            nonfocal += 1
            stroke = strokes.get(name, f"rgba(45,49,66,{alpha})")
            width = widths.get(name, "1.2")
        tr = f' transform="{path_transform[name]}"' if path_transform.get(name) else ""
        ranks_attr_str = (
            "" if f"ranksattr:{name}" in drop else f' data-ranks="{ranks_str}"'
        )
        parts.append(
            f'<path data-series="{name}"{ranks_attr_str} d="{d}" fill="none"'
            f' stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"{tr}/>'
        )
        for i, (x, y) in enumerate(vertices):
            if f"dot:{name}:{i}" in dot_drop:
                continue
            r = dot_r.get((name, i), 4 if focal else 3)
            fill = stroke if focal else "#2d3142"
            parts.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="{fill}"/>')

    for name, ranks, _focal in series:
        for end in ("first", "last"):
            rank = ranks[0] if end == "first" else ranks[-1]
            for role in ("name", "rank"):
                if f"label:{name}:{end}:{role}" in drop:
                    continue
                key = (name, end, role)
                lx = label_x.get(key, gutter[(end, role)])
                ly_role = row_y(rank) + 3.5 + label_dy.get(key, 0)
                if role == "name":
                    text = label_texts.get(key, name)
                    anchor = ' text-anchor="end"' if end == "first" else ""
                    fill = "#2d3142"
                    size = "11"
                else:
                    text = label_texts.get(key, f"#{rank}")
                    anchor = ' text-anchor="end"' if end == "first" else ""
                    fill = "#4f5d75"
                    size = "9"
                end_attr = label_end.get(key, end)
                role_attr = (
                    ""
                    if f"role:label:{name}:{end}:{role}" in drop
                    else f' data-role="{role}"'
                )
                parts.append(
                    f'<text data-series="{name}" data-end="{end_attr}"{role_attr}'
                    f' x="{fmt(lx)}" y="{fmt(ly_role)}" fill="{fill}" font-size="{size}"'
                    f" font-family=\"'Geist', sans-serif\"{anchor}>{text}</text>"
                )

    if group_transform is not None:
        parts.append("</g>")

    for idx, (axis_idx, state) in enumerate(captions):
        if f"capt:{idx}" in drop:
            continue
        cx = caption_x.get(idx, col_x[axis_idx] if axis_idx < len(col_x) else col_x[-1])
        axis_attr = (
            ""
            if f"axis:capt:{idx}" in drop
            else f' data-axis="{caption_axis.get(idx, axis_idx)}"'
        )
        text = caption_texts.get(idx, state)
        parts.append(
            f'<text{axis_attr} data-state="{state}" x="{fmt(cx)}" y="416" fill="#4f5d75"'
            f' font-size="9" font-family="\'Geist Mono\', monospace" letter-spacing="0.14em"'
            f' text-anchor="middle">{text}</text>'
        )

    parts.append(extra_svg)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">\n'
        + "\n".join(parts)
        + "\n</svg>\n"
    )


def run_gate(svg: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "figure.svg"
        path.write_text(svg, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(GATE), str(path)],
            capture_output=True,
            text=True,
        )
    return proc.returncode, proc.stdout + proc.stderr


THREE_SERIES = [
    ("alpha", [1, 2, 3], True),
    ("beta", [2, 3, 1], False),
    ("gamma", [3, 1, 2], False),
]
TWO_SNAPSHOTS = [
    ("alpha", [1, 2], True),
    ("beta", [2, 1], False),
    ("gamma", [3, 4], False),
    ("delta", [4, 3], False),
]
TIE_SERIES = [
    ("alpha", [1, 1, 3], True),
    ("beta", [2, 1, 4], False),
    ("gamma", [3, 4, 1], False),
    ("delta", [4, 3, 2], False),
]
TRUNCATED_SERIES = [
    ("alpha", [1, 2], True),
    ("beta", [2, 1, 4], False),
    ("gamma", [3, 4, 1], False),
    ("delta", [4, 3, 2], False),
]
DUP_ALPHA_PATH = (
    '<path data-series="alpha" data-ranks="1,2,3" d="M320,88 L440,144 L560,200"'
    ' fill="none" stroke="#eb6c36" stroke-width="2.4"/>'
)
DUP_ALPHA_LABEL = (
    '<text data-series="alpha" data-end="first" data-role="name" x="272" y="91.5"'
    ' fill="#2d3142" font-size="11" text-anchor="end">alpha</text>'
)
ROTATED_DECORATION = (
    '<text transform="rotate(-90 24 250)" x="24" y="250" fill="#4f5d75" font-size="9"'
    " font-family=\"'Geist Mono', monospace\">RANK</text>"
)
ALL_FIRST_NAMES_IN_PLOT = {(name, "first", "name"): 330 for name, _, _ in BASE_SERIES}

CASES = [
    ("base figure passes every check", build(), 0, None),
    ("scope treaty: ridgeline-only file is not claimed", RIDGE_ONLY_SVG, 0, None),
    (
        "transform exemption: rotated unbound decoration stays legal",
        build(extra_svg=ROTATED_DECORATION),
        0,
        None,
    ),
    (
        "grid_row: vertex nudged off its row",
        build(d_override={"alpha": "M320,89 L440,144 L560,200"}),
        1,
        "grid_row",
    ),
    (
        "rank_permutation: duplicated rank in one snapshot",
        build(series=TIE_SERIES),
        1,
        "rank_permutation",
    ),
    (
        "visit_incomplete: series stops before the last snapshot",
        build(series=TRUNCATED_SERIES),
        1,
        "visit_incomplete",
    ),
    (
        "ranks_length: more ranks than vertices",
        build(ranks_attr={"alpha": "1,2,3,4"}),
        1,
        "ranks_length",
    ),
    (
        "ranks_unparsable: non-integer rank",
        build(ranks_attr={"alpha": "1,x,3"}),
        1,
        "ranks_unparsable",
    ),
    (
        "segment_grammar: smoothed segment",
        build(d_override={"beta": "M320,144 Q380,120 440,88 L560,256"}),
        1,
        "segment_grammar",
    ),
    (
        "column_x_mismatch: vertex off its snapshot column",
        build(d_override={"beta": "M320,144 L445,88 L560,256"}),
        1,
        "column_x_mismatch",
    ),
    (
        "binding_path_incomplete: data-ranks stripped",
        build(drop=("ranksattr:alpha",)),
        1,
        "binding_path_incomplete",
    ),
    (
        "duplicate_series: second path for one series",
        build(extra_svg=DUP_ALPHA_PATH),
        1,
        "duplicate_series",
    ),
    (
        "dot_missing: vertex without a dot",
        build(dot_drop=("dot:alpha:1",)),
        1,
        "dot_missing",
    ),
    (
        "dot_radius: non-focal dot at focal size",
        build(dot_r={("beta", 0): 4}),
        1,
        "dot_radius",
    ),
    (
        "focus_pairing: two series carry the heavy weight",
        build(widths={"beta": "2.4"}),
        1,
        "focus_pairing",
    ),
    (
        "ink_ramp_mismatch: second hue in the ramp",
        build(strokes={"beta": "#7c8f6f"}),
        1,
        "ink_ramp_mismatch",
    ),
    ("series_count: three series", build(series=THREE_SERIES), 1, "series_count"),
    (
        "snapshot_count: two snapshots",
        build(series=TWO_SNAPSHOTS, col_x=[320, 440], captions=[(0, "Q1"), (1, "Q2")]),
        1,
        "snapshot_count",
    ),
    (
        "label_missing: last-end name dropped",
        build(drop=("label:alpha:last:name",)),
        1,
        "label_missing",
    ),
    (
        "label_duplicate: second first-end name",
        build(extra_svg=DUP_ALPHA_LABEL),
        1,
        "label_duplicate",
    ),
    (
        "label_binding_incomplete: data-role stripped",
        build(drop=("role:label:alpha:first:rank",)),
        1,
        "label_binding_incomplete",
    ),
    (
        "label_end_unknown: data-end outside first/last",
        build(label_end={("alpha", "first", "rank"): "middle"}),
        1,
        "label_end_unknown",
    ),
    (
        "name_mismatch: name text off its binding",
        build(label_texts={("alpha", "first", "name"): "ALPHA"}),
        1,
        "name_mismatch",
    ),
    (
        "rank_mismatch: printed rank off its binding",
        build(label_texts={("alpha", "first", "rank"): "#2"}),
        1,
        "rank_mismatch",
    ),
    (
        "label_off_row: label slid off its series' row",
        build(label_dy={("alpha", "first", "name"): 10}),
        1,
        "label_off_row",
    ),
    (
        "gutter_column: one label off the shared column",
        build(label_x={("alpha", "first", "name"): 280}),
        1,
        "gutter_column",
    ),
    (
        "gutter_side: first-end labels inside the plot",
        build(label_x=ALL_FIRST_NAMES_IN_PLOT),
        1,
        "gutter_side",
    ),
    (
        "caption_text_mismatch: caption text off data-state",
        build(caption_texts={0: "Q9"}),
        1,
        "caption_text_mismatch",
    ),
    (
        "caption_binding: data-axis stripped",
        build(drop=("axis:capt:0",)),
        1,
        "caption_binding",
    ),
    (
        "caption_position: caption off its snapshot column",
        build(caption_x={0: 330}),
        1,
        "caption_position",
    ),
    (
        "caption_axis: data-axis outside the snapshots",
        build(caption_axis={0: "5"}),
        1,
        "caption_axis",
    ),
    (
        "caption_missing: last snapshot caption dropped",
        build(drop=("capt:2",)),
        1,
        "caption_missing",
    ),
    (
        "transform_forbidden: transform on a bound path",
        build(path_transform={"alpha": "translate(0 8)"}),
        1,
        "transform_forbidden",
    ),
    (
        "transform_forbidden: transform on an ancestor g",
        build(group_transform="translate(0 8)"),
        1,
        "transform_forbidden",
    ),
    (
        "transform_forbidden: transform in a CSS rule",
        build(style=".series { transform: translateY(8px); }"),
        1,
        "transform_forbidden",
    ),
]


def main() -> int:
    failures = []
    for name, svg, expect_code, expect_rule in CASES:
        code, output = run_gate(svg)
        problems = []
        if code != expect_code:
            problems.append(f"exit {code}, expected {expect_code}")
        if expect_rule is None:
            if output.strip():
                problems.append(f"expected no findings, got: {output.strip()[:400]}")
        elif expect_rule not in output:
            problems.append(
                f"rule '{expect_rule}' did not fire; output: {output.strip()[:400]}"
            )
        if problems:
            failures.append(name)
            print(f"FAIL {name}: {'; '.join(problems)}")
        else:
            print(f"ok   {name}")
    total = len(CASES)
    print(f"\n{total - len(failures)}/{total} cases passed")
    if failures:
        print("failed: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
