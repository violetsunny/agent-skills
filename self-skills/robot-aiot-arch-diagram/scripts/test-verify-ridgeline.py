#!/usr/bin/env python3
"""Both-polarity tests for verify-ridgeline.py.

Contract source: references/type-line.md, section "Variants > Ridgeline":
"scripts/test-verify-ridgeline.py proves each check in both polarities and
pins the scope treaty with the sibling gates."

Every check gets a passing polarity and a violating polarity. The passing
polarity for all checks at once is the base fixture (a complete, honest
three-ridge figure that must exit 0 with no output); targeted passing
variants prove the exemptions (rotated unbound caption, out-of-scope file).
Each violating fixture is the base figure with exactly one deliberate defect,
built from parameters rather than string surgery so geometry stays
self-consistent. A violation case asserts exit code 1 and that the target
rule fires; incidental findings caused by the same defect are tolerated.

The scope treaty case pins that this gate never reads data-series: a file
speaking only the slopegraph's vocabulary exits 0 with no findings and no
mention of data-bins - the gate does not claim the other's file.

Fixtures are synthetic SVG strings; no external files are read.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-ridgeline.py"

X0 = 320
STEP = 30
AMPLITUDE = 2.4
INK_ALPHAS = ("0.8", "0.71", "0.62", "0.66", "0.75")

BASE_RIDGES = [
    ("alpha-svc", 200, [0, 3, 8, 12, 9, 4, 1, 0], True),
    ("beta-svc", 256, [0, 1, 4, 10, 14, 6, 2, 0], False),
    ("gamma-svc", 312, [0, 0, 6, 9, 11, 5, 0, 0], False),
]
BASE_TICKS = [(0, 320, 40), (3, 410, 130), (6, 500, 220)]

SLOPEGRAPH_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<line data-series="Recommender" data-from="238" data-to="431" x1="320" y1="303.5" x2="680" y2="140.5" stroke="#eb6c36" stroke-width="2.4"/>
<text data-series="Recommender" data-end="from" data-role="name" x="272" y="307" text-anchor="end">Recommender</text>
<text data-series="Recommender" data-end="from" x="304" y="307" text-anchor="end">238</text>
</svg>
"""


def fmt(value: float) -> str:
    rounded = round(value, 6)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:g}"


def tick_scale(ticks):
    (_, xa, va), (_, xb, vb) = ticks[0], ticks[1]
    m = (vb - va) / (xb - xa)
    return m, va - m * xa


def build(
    ridges=None,
    ticks=None,
    scales=None,
    widths=None,
    strokes=None,
    fills=None,
    bins_attr=None,
    d_override=None,
    x_shift=None,
    ridge_transform=None,
    rule_dy=None,
    rule_x2=None,
    drop=(),
    tick_texts=None,
    range_texts=None,
    name_texts=None,
    label_dy=None,
    name_x=None,
    range_x=None,
    group_transform=None,
    style=None,
    extra_svg="",
):
    ridges = BASE_RIDGES if ridges is None else ridges
    ticks = BASE_TICKS if ticks is None else ticks
    scales = scales or {}
    widths = widths or {}
    strokes = strokes or {}
    fills = fills or {}
    bins_attr = bins_attr or {}
    d_override = d_override or {}
    x_shift = x_shift or {}
    ridge_transform = ridge_transform or {}
    rule_dy = rule_dy or {}
    rule_x2 = rule_x2 or {}
    drop = set(drop)
    tick_texts = tick_texts or {}
    range_texts = range_texts or {}
    name_texts = name_texts or {}
    label_dy = label_dy or {}
    name_x = name_x or {}
    range_x = range_x or {}

    m, c = tick_scale(ticks) if len(ticks) >= 2 else (1.0, -280.0)
    parts = []
    if style:
        parts.append(f"<style>{style}</style>")
    if group_transform is not None:
        parts.append(f'<g transform="{group_transform}">')

    nonfocal = 0
    for rid, baseline, bins, focal in ridges:
        n = len(bins)
        xlist = [X0 + STEP * i + x_shift.get(rid, 0) for i in range(n)]
        a = scales.get(rid, AMPLITUDE)
        ys = [baseline - a * b for b in bins]
        d = d_override.get(rid) or (
            "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in zip(xlist, ys)) + " Z"
        )
        bins_str = bins_attr.get(rid) or ",".join(str(b) for b in bins)
        if focal:
            stroke = strokes.get(rid, "#eb6c36")
            width = widths.get(rid, "2.4")
            fill = fills.get(rid, "rgba(235,108,54,0.16)")
        else:
            alpha = INK_ALPHAS[nonfocal % len(INK_ALPHAS)]
            nonfocal += 1
            stroke = strokes.get(rid, f"rgba(45,49,66,{alpha})")
            width = widths.get(rid, "1.2")
            fill = fills.get(rid, "rgba(45,49,66,0.12)")
        baseline_attr = (
            "" if f"pathbaseline:{rid}" in drop else f' data-baseline="{fmt(baseline)}"'
        )
        tr = f' transform="{ridge_transform[rid]}"' if ridge_transform.get(rid) else ""
        parts.append(
            f'<path data-ridge="{rid}"{baseline_attr} data-bins="{bins_str}" d="{d}"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"{tr}/>'
        )
        if f"rule:{rid}" not in drop:
            ry = baseline + rule_dy.get(rid, 0)
            rx2 = rule_x2.get(rid, xlist[-1])
            parts.append(
                f'<line data-ridge="{rid}" data-role="baseline" x1="{fmt(xlist[0])}" y1="{fmt(ry)}"'
                f' x2="{fmt(rx2)}" y2="{fmt(ry)}" stroke="rgba(45,49,66,0.25)" stroke-width="1"/>'
            )
        nonzero = [i for i, b in enumerate(bins) if b != 0]
        if nonzero and len(ticks) >= 2:
            default_range = f"{fmt(m * xlist[nonzero[0]] + c)}\u2013{fmt(m * xlist[nonzero[-1]] + c)} ms"
        else:
            default_range = "70\u2013220 ms"
        ly = baseline + 3.5 + label_dy.get(rid, 0)
        if f"name:{rid}" not in drop:
            role_attr = "" if f"role:name:{rid}" in drop else ' data-role="name"'
            parts.append(
                f'<text data-ridge="{rid}"{role_attr} x="{fmt(name_x.get(rid, 304))}" y="{fmt(ly)}"'
                f' fill="#2d3142" font-size="11" font-family="\'Geist\', sans-serif"'
                f' text-anchor="end">{name_texts.get(rid, rid)}</text>'
            )
        if f"range:{rid}" not in drop:
            parts.append(
                f'<text data-ridge="{rid}" data-role="range" x="{fmt(range_x.get(rid, 546))}"'
                f' y="{fmt(ly)}" fill="#4f5d75" font-size="9"'
                f" font-family=\"'Geist Mono', monospace\">{range_texts.get(rid, default_range)}</text>"
            )

    if group_transform is not None:
        parts.append("</g>")

    for idx, (tidx, tx, tval) in enumerate(ticks):
        if f"tick:{idx}" in drop:
            continue
        bin_attr = "" if f"tickbin:{idx}" in drop else f' data-bin="{fmt(tval)}"'
        parts.append(
            f'<text data-tick="{tidx}"{bin_attr} x="{fmt(tx)}" y="400" fill="#4f5d75"'
            f' font-size="9" font-family="\'Geist Mono\', monospace" letter-spacing="0.14em"'
            f' text-anchor="middle">{tick_texts.get(idx, fmt(tval))}</text>'
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


BETA_D_OPEN = (
    "M320,256 L350,253.6 L380,246.4 L410,232 L440,222.4 L470,241.6 L500,251.2 L530,256"
)
BETA_D_CURVE = (
    "M320,256 C350,253.6 380,246.4 410,232 L440,222.4 L470,241.6 L500,251.2 L530,256 Z"
)
BETA_D_JITTER = "M320,256 L350,253.6 L385,246.4 L410,232 L440,222.4 L470,241.6 L500,251.2 L530,256 Z"
BETA_D_CLIFF_Y = "M320,250 L350,253.6 L380,246.4 L410,232 L440,222.4 L470,241.6 L500,251.2 L530,256 Z"
DUP_BETA_PATH = (
    '<path data-ridge="beta-svc" data-baseline="256" data-bins="0,1,4,10,14,6,2,0"'
    f' d="{BETA_D_OPEN} Z" fill="rgba(45,49,66,0.12)" stroke="rgba(45,49,66,0.8)"'
    ' stroke-width="1.2"/>'
)
DUP_GAMMA_NAME = (
    '<text data-ridge="gamma-svc" data-role="name" x="304" y="315.5" fill="#2d3142"'
    ' font-size="11" text-anchor="end">gamma-svc</text>'
)
ROTATED_CAPTION = (
    '<text transform="rotate(-90 24 250)" x="24" y="250" fill="#4f5d75" font-size="9"'
    " font-family=\"'Geist Mono', monospace\">REQUESTS</text>"
)

TWO_RIDGES = BASE_RIDGES[:2]
GAMMA_7 = [
    BASE_RIDGES[0],
    BASE_RIDGES[1],
    ("gamma-svc", 312, [0, 6, 9, 11, 5, 2, 0], False),
]
GAMMA_9 = [
    BASE_RIDGES[0],
    BASE_RIDGES[1],
    ("gamma-svc", 312, [0, 0, 6, 9, 11, 5, 2, 1, 0], False),
]
GAMMA_SHIFTED = [
    BASE_RIDGES[0],
    BASE_RIDGES[1],
    ("gamma-svc", 316, [0, 0, 6, 9, 11, 5, 0, 0], False),
]
BETA_CLIFF = [
    BASE_RIDGES[0],
    ("beta-svc", 256, [1, 1, 4, 10, 14, 6, 2, 0], False),
    BASE_RIDGES[2],
]
BETA_TALL = [
    BASE_RIDGES[0],
    ("beta-svc", 256, [0, 1, 4, 10, 26, 6, 2, 0], False),
    BASE_RIDGES[2],
]

CASES = [
    ("base figure passes every check", build(), 0, None),
    (
        "scope treaty: slopegraph-only file is not claimed",
        SLOPEGRAPH_ONLY_SVG,
        0,
        None,
    ),
    (
        "transform exemption: rotated unbound caption stays legal",
        build(extra_svg=ROTATED_CAPTION),
        0,
        None,
    ),
    (
        "binding_path_incomplete: data-baseline stripped",
        build(drop=("pathbaseline:beta-svc",)),
        1,
        "binding_path_incomplete",
    ),
    (
        "bins_unparsable: non-numeric bin",
        build(bins_attr={"beta-svc": "0,1,x,10,14,6,2,0"}),
        1,
        "bins_unparsable",
    ),
    (
        "duplicate_ridge: second outline for one ridge",
        build(extra_svg=DUP_BETA_PATH),
        1,
        "duplicate_ridge",
    ),
    ("ridge_count: two ridges", build(ridges=TWO_RIDGES), 1, "ridge_count"),
    ("bin_count: seven bins", build(ridges=GAMMA_7), 1, "bin_count"),
    (
        "bin_count_mismatch: ridges sampled differently",
        build(ridges=GAMMA_9),
        1,
        "bin_count_mismatch",
    ),
    (
        "segment_grammar: spline command",
        build(d_override={"beta-svc": BETA_D_CURVE}),
        1,
        "segment_grammar",
    ),
    (
        "segment_grammar: outline not closed with Z",
        build(d_override={"beta-svc": BETA_D_OPEN}),
        1,
        "segment_grammar",
    ),
    (
        "amplitude_violation: per-ridge normalisation",
        build(scales={"beta-svc": 3.6}),
        1,
        "amplitude_violation",
    ),
    (
        "pitch_uneven: baseline nudged off the pitch",
        build(ridges=GAMMA_SHIFTED),
        1,
        "pitch_uneven",
    ),
    (
        "overlap_ceiling: peak reaches the row two above",
        build(ridges=BETA_TALL),
        1,
        "overlap_ceiling",
    ),
    (
        "baseline_rule_missing: rule dropped",
        build(drop=("rule:beta-svc",)),
        1,
        "baseline_rule_missing",
    ),
    (
        "baseline_rule_mismatch: rule drawn off the declared row",
        build(rule_dy={"beta-svc": 4}),
        1,
        "baseline_rule_mismatch",
    ),
    (
        "baseline_rule_span: rule shorter than the bin run",
        build(rule_x2={"beta-svc": 500}),
        1,
        "baseline_rule_span",
    ),
    ("ridge_cliff: first bin nonzero", build(ridges=BETA_CLIFF), 1, "ridge_cliff"),
    (
        "ridge_not_closed_on_baseline: outline starts off its baseline",
        build(d_override={"beta-svc": BETA_D_CLIFF_Y}),
        1,
        "ridge_not_closed_on_baseline",
    ),
    (
        "x_range_mismatch: ridge sampled on a shifted x-range",
        build(x_shift={"beta-svc": 10}),
        1,
        "x_range_mismatch",
    ),
    (
        "x_grid_uneven: vertex off the evenly spaced grid",
        build(d_override={"beta-svc": BETA_D_JITTER}),
        1,
        "x_grid_uneven",
    ),
    (
        "focus_pairing: two ridges carry the heavy weight",
        build(widths={"beta-svc": "2.4"}),
        1,
        "focus_pairing",
    ),
    (
        "focus_pairing: focal stroke is an ink-ramp member",
        build(strokes={"alpha-svc": "rgba(45,49,66,0.86)"}),
        1,
        "focus_pairing",
    ),
    (
        "ink_ramp_mismatch: second hue in the ramp",
        build(strokes={"beta-svc": "#7c8f6f"}),
        1,
        "ink_ramp_mismatch",
    ),
    (
        "fill_hue_mismatch: fill hue off its stroke hue",
        build(fills={"beta-svc": "rgba(124,143,111,0.12)"}),
        1,
        "fill_hue_mismatch",
    ),
    (
        "label_missing: range label dropped",
        build(drop=("range:gamma-svc",)),
        1,
        "label_missing",
    ),
    (
        "label_duplicate: second name label",
        build(extra_svg=DUP_GAMMA_NAME),
        1,
        "label_duplicate",
    ),
    (
        "label_binding_incomplete: data-role stripped",
        build(drop=("role:name:gamma-svc",)),
        1,
        "label_binding_incomplete",
    ),
    (
        "name_mismatch: name text off its binding",
        build(name_texts={"gamma-svc": "delta-svc"}),
        1,
        "name_mismatch",
    ),
    (
        "range_mismatch: range widened by a word",
        build(range_texts={"gamma-svc": "100\u2013200 ms"}),
        1,
        "range_mismatch",
    ),
    (
        "range_format: range prints one number",
        build(range_texts={"gamma-svc": "100 ms"}),
        1,
        "range_format",
    ),
    (
        "label_off_row: label slid off its ridge's row",
        build(label_dy={"gamma-svc": 10}),
        1,
        "label_off_row",
    ),
    (
        "label_side: name label on the wrong side of the run",
        build(name_x={"gamma-svc": 700}),
        1,
        "label_side",
    ),
    ("tick_binding: data-bin stripped", build(drop=("tickbin:1",)), 1, "tick_binding"),
    (
        "tick_text_mismatch: printed tick off its binding",
        build(tick_texts={1: "131"}),
        1,
        "tick_text_mismatch",
    ),
    (
        "tick_off_bin: tick centred between bins",
        build(ticks=[(0, 320, 40), (3, 415, 130), (6, 500, 220)]),
        1,
        "tick_off_bin",
    ),
    (
        "tick_scale_inconsistent: ticks off one linear scale",
        build(ticks=[(0, 320, 40), (3, 410, 130), (6, 500, 260)]),
        1,
        "tick_scale_inconsistent",
    ),
    (
        "xscale_unprinted: a single tick prints no scale",
        build(ticks=[(0, 320, 40)]),
        1,
        "xscale_unprinted",
    ),
    (
        "transform_forbidden: transform on a bound outline",
        build(ridge_transform={"beta-svc": "translate(0 8)"}),
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
        build(style=".ridge { transform: translateY(8px); }"),
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
            if "scope treaty" in name and "data-bins" in output:
                problems.append("gate mentioned data-bins for an out-of-scope file")
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
