#!/usr/bin/env python3
"""Both-polarity tests for verify-beeswarm.py.

Contract source: references/type-scatter.md, section "Beeswarm":
"scripts/test-verify-beeswarm.py proves each check in both polarities and
pins the sibling scope treaty in both directions."

Every check gets a passing polarity and a violating polarity. The passing
polarity for all checks at once is the base fixture (a complete, honest
20-dot swarm that must exit 0 with no output); targeted passing variants
prove the exemptions (non-positioning inline style, out-of-scope files).
Each violating fixture is the base figure with exactly one deliberate defect,
built from parameters rather than string surgery so geometry stays
self-consistent. A violation case asserts exit code 1 and that the target
rule fires; incidental findings caused by the same defect are tolerated.

The scope treaty is pinned in both directions: files speaking only a
sibling's vocabulary (data-series slopegraph, data-bins ridgeline,
data-ranks bump, data-size bubble) exit 0 with no findings under this gate,
and the base beeswarm figure - which carries none of their vocabulary -
exits 0 with no findings under each sibling gate.

Fixtures are synthetic SVG strings; no external files are read.
"""

from __future__ import annotations

import math
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-beeswarm.py"
SIBLING_GATES = [
    "verify-slopegraph.py",
    "verify-ridgeline.py",
    "verify-bump.py",
    "verify-bubble.py",
]

BASE_VALUES = [
    10,
    20,
    30,
    40,
    50,
    50,
    60,
    70,
    80,
    90,
    100,
    110,
    120,
    130,
    140,
    150,
    160,
    170,
    180,
    400,
]
X0 = 80.0
B = 2.0
R = 4.0
MID = 230.0
PITCH = 10.0
INK_FILL = "rgba(45,49,66,0.55)"
ACCENT_FILL = "rgba(235,108,54,0.55)"
BASE_TICK_VALUES = [0, 100, 200, 300, 400]

SLOPE_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<line data-series="alpha" data-from="10" data-to="30" x1="320" y1="300" x2="680" y2="100" stroke="#4f5d75" stroke-width="1.2"/>
<text data-series="alpha" data-end="from" data-role="name" x="272" y="303.5">alpha</text>
</svg>
"""

RIDGE_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<path data-ridge="checkout-api" data-baseline="320" data-bins="0,1,6,17,21,14,8,6,7,9,7,4,0" d="M320,320 L350,317.6 L380,305.6 L410,279.2 L440,269.6 L470,286.4 L500,300.8 L530,305.6 L560,303.2 L590,298.4 L620,303.2 L650,310.4 L680,320 Z" fill="rgba(235,108,54,0.16)" stroke="#eb6c36" stroke-width="2.4"/>
</svg>
"""

BUMP_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<path data-series="alpha" data-ranks="1,2,3" d="M320,88 L440,144 L560,200" fill="none" stroke="#eb6c36" stroke-width="2.4"/>
</svg>
"""

BUBBLE_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<circle cx="300" cy="300" r="20" fill="#f5f5f5"/>
<circle data-name="Payments" data-x="260" data-y="2.8" data-size="760" cx="300" cy="300" r="20" fill="rgba(235,108,54,0.15)" stroke="#eb6c36" stroke-width="1.2"/>
<text data-name="Payments" data-role="label" x="300" y="270" font-size="8" text-anchor="middle">PAYMENTS</text>
<text data-tick="x" data-value="300" x="608" y="440" font-size="8" text-anchor="middle">300</text>
</svg>
"""


def fmt(value: float) -> str:
    rounded = round(value, 6)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:g}"


def build(
    values=None,
    focal=None,
    names=None,
    dot_cx=None,
    dot_cy=None,
    dot_r=None,
    dot_fill=None,
    dot_name=None,
    dot_value=None,
    dot_style=None,
    dot_transform=None,
    labels=None,
    ticks=None,
    style=None,
    group_transform=None,
    extra_svg=None,
):
    values = BASE_VALUES if values is None else values
    focal = len(values) - 1 if focal is None else focal
    dot_cx = dot_cx or {}
    dot_cy = dot_cy or {}
    dot_r = dot_r or {}
    dot_fill = dot_fill or {}
    dot_value = dot_value or {}
    dot_style = dot_style or {}
    dot_transform = dot_transform or {}

    final_names = {0: "req-a", len(values) - 2: "req-b", focal: "req-4c1f"}
    if names is not None:
        final_names = dict(names)
    if dot_name:
        final_names.update(dot_name)
        final_names = {k: v for k, v in final_names.items() if v is not None}

    placed = []
    for v in values:
        cx = X0 + B * v
        k = 0
        while True:
            if k == 0:
                off = 0.0
            else:
                steps = (k + 1) // 2
                off = steps * PITCH * (-1 if k % 2 else 1)
            cy = MID + off
            if all(math.hypot(cx - px, cy - py) >= 2 * R + 0.5 for px, py in placed):
                break
            k += 1
        placed.append((cx, cy))

    parts = []
    if style:
        parts.append(f"<style>{style}</style>")
    if group_transform is not None:
        parts.append(f'<g transform="{group_transform}">')

    for i, v in enumerate(values):
        cx = dot_cx.get(i, placed[i][0])
        cy = dot_cy.get(i, placed[i][1])
        r = dot_r.get(i, R)
        is_focal = i == focal
        fill = dot_fill.get(i, ACCENT_FILL if is_focal else INK_FILL)
        if is_focal and i not in dot_fill:
            stroke, sw = "#eb6c36", "1.2"
        else:
            stroke, sw = "#4f5d75", "0.75"
        value_attr = dot_value.get(i, fmt(v))
        name = final_names.get(i)
        name_attr = f' data-name="{name}"' if name is not None else ""
        style_attr = f' style="{dot_style[i]}"' if i in dot_style else ""
        tr_attr = f' transform="{dot_transform[i]}"' if i in dot_transform else ""
        parts.append(
            f'<circle data-value="{value_attr}"{name_attr} cx="{fmt(cx)}" cy="{fmt(cy)}"'
            f' r="{fmt(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
            f"{style_attr}{tr_attr}/>"
        )

    if labels is None:
        labels = [
            {
                "name": final_names[i],
                "text": final_names[i].upper(),
                "x": dot_cx.get(i, placed[i][0]),
                "y": 120,
                "role": "label",
            }
            for i in sorted(final_names)
        ]
    for lab in labels:
        role_attr = f' data-role="{lab["role"]}"' if lab.get("role") else ""
        parts.append(
            f'<text data-name="{lab["name"]}"{role_attr} x="{fmt(lab["x"])}" y="{fmt(lab["y"])}"'
            f' fill="#2d3142" font-size="8" font-family="\'Geist Mono\', monospace"'
            f' text-anchor="middle" letter-spacing="0.06em">{lab["text"]}</text>'
        )

    if ticks is None:
        ticks = [
            {"tick": "x", "value": v, "x": X0 + B * v, "text": fmt(v)}
            for v in BASE_TICK_VALUES
        ]
    for t in ticks:
        tick_attr = f' data-tick="{t["tick"]}"' if t.get("tick") else ""
        value_attr = f' data-value="{t["value"]}"' if t.get("value") is not None else ""
        parts.append(
            f'<text{tick_attr}{value_attr} x="{fmt(t["x"])}" y="440" fill="#4f5d75"'
            f' font-size="8" font-family="\'Geist Mono\', monospace"'
            f' text-anchor="middle">{t["text"]}</text>'
        )

    if group_transform is not None:
        parts.append("</g>")
    if extra_svg:
        parts.append(extra_svg)

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">\n'
        + "\n".join(parts)
        + "\n</svg>\n"
    )


def run_gate(svg: str, gate: Path = GATE) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "figure.svg"
        path.write_text(svg, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(gate), str(path)],
            capture_output=True,
            text=True,
        )
    return proc.returncode, proc.stdout + proc.stderr


def ticks_from(values, axis="x"):
    return [{"tick": axis, "value": v, "x": X0 + B * v, "text": fmt(v)} for v in values]


BASE = build()

OVERPRINT_DOT = (
    '<circle data-value="100" cx="280" cy="233" r="4" fill="rgba(45,49,66,0.55)"'
    ' stroke="#4f5d75" stroke-width="0.75"/>'
)
GHOST_LABEL = (
    '<text data-name="ghost" data-role="label" x="500" y="120" fill="#2d3142"'
    ' font-size="8" text-anchor="middle">GHOST</text>'
)
SEVEN_NAMES = {
    0: "req-a",
    2: "req-c",
    4: "req-d",
    6: "req-e",
    8: "req-f",
    18: "req-b",
    19: "req-4c1f",
}

CASES = [
    ("base figure passes every check", BASE, 0, None),
    ("scope treaty: slopegraph-only file is not claimed", SLOPE_ONLY_SVG, 0, None),
    ("scope treaty: ridgeline-only file is not claimed", RIDGE_ONLY_SVG, 0, None),
    ("scope treaty: bump-only file is not claimed", BUMP_ONLY_SVG, 0, None),
    ("scope treaty: bubble-only file is not claimed", BUBBLE_ONLY_SVG, 0, None),
    (
        "carrier exemption: non-positioning inline style stays legal",
        build(dot_style={5: "color: #2d3142; line-height: 1.2"}),
        0,
        None,
    ),
    (
        "dot_count: nineteen dots",
        build(values=BASE_VALUES[:19]),
        1,
        "dot_count",
    ),
    (
        "dot_count: three hundred one dots",
        build(values=[5 * i for i in range(301)]),
        1,
        "dot_count",
    ),
    (
        "value_off_scale: dot nudged along the value axis",
        build(dot_cx={10: 283}),
        1,
        "value_off_scale",
    ),
    (
        "scale_unverifiable: every dot carries one value",
        build(values=[50] * 20),
        1,
        "scale_unverifiable",
    ),
    (
        "same_value_position: equal values dodged apart on the value axis",
        build(dot_cx={5: 180.4}),
        1,
        "same_value_position",
    ),
    (
        "overprint: stray dot painted on a neighbour",
        build(extra_svg=OVERPRINT_DOT),
        1,
        "overprint",
    ),
    (
        "dot_radius: one dot at a second radius",
        build(dot_r={5: 5}),
        1,
        "dot_radius",
    ),
    (
        "nonfocal_fill: deviating fill on an unnamed dot",
        build(dot_fill={5: "rgba(45,49,66,0.56)"}),
        1,
        "nonfocal_fill",
    ),
    (
        "accent_cap: two accent dots",
        build(
            dot_fill={5: ACCENT_FILL},
            dot_name={5: "req-x"},
        ),
        1,
        "accent_cap",
    ),
    (
        "name_empty: focal dot with an empty data-name",
        build(dot_name={19: ""}),
        1,
        "name_empty",
    ),
    (
        "name_duplicate: two dots wearing one data-name",
        build(dot_name={18: "req-a"}),
        1,
        "name_duplicate",
    ),
    (
        "label_cap: seven bound labels",
        build(names=SEVEN_NAMES),
        1,
        "label_cap",
    ),
    (
        "label_target_unknown: label names a dot that is not there",
        build(extra_svg=GHOST_LABEL),
        1,
        "label_target_unknown",
    ),
    (
        "label_text_mismatch: printed name off its binding",
        build(
            labels=[
                {
                    "name": "req-4c1f",
                    "text": "WRONG",
                    "x": 880,
                    "y": 120,
                    "role": "label",
                },
                {"name": "req-a", "text": "REQ-A", "x": 100, "y": 120, "role": "label"},
                {"name": "req-b", "text": "REQ-B", "x": 440, "y": 140, "role": "label"},
            ]
        ),
        1,
        "label_text_mismatch",
    ),
    (
        "label_binding_incomplete: label without data-role",
        build(
            labels=[
                {
                    "name": "req-4c1f",
                    "text": "REQ-4C1F",
                    "x": 880,
                    "y": 120,
                    "role": None,
                },
            ]
        ),
        1,
        "label_binding_incomplete",
    ),
    (
        "binding_value_unparsable: non-numeric data-value on a dot",
        build(dot_value={5: "abc"}),
        1,
        "binding_value_unparsable",
    ),
    (
        "tick_text_mismatch: tick prints a number off its binding",
        build(
            ticks=[
                {"tick": "x", "value": 0, "x": 80, "text": "0"},
                {"tick": "x", "value": 100, "x": 280, "text": "999"},
                {"tick": "x", "value": 200, "x": 480, "text": "200"},
                {"tick": "x", "value": 300, "x": 680, "text": "300"},
                {"tick": "x", "value": 400, "x": 880, "text": "400"},
            ]
        ),
        1,
        "tick_text_mismatch",
    ),
    (
        "tick_off_scale: tick drawn off the shared scale",
        build(
            ticks=[
                {"tick": "x", "value": 0, "x": 80, "text": "0"},
                {"tick": "x", "value": 100, "x": 288, "text": "100"},
                {"tick": "x", "value": 200, "x": 480, "text": "200"},
                {"tick": "x", "value": 300, "x": 680, "text": "300"},
                {"tick": "x", "value": 400, "x": 880, "text": "400"},
            ]
        ),
        1,
        "tick_off_scale",
    ),
    (
        "tick_count: three bound ticks",
        build(ticks=ticks_from([0, 100, 200])),
        1,
        "tick_count",
    ),
    (
        "tick_spacing: ticks at unequal intervals",
        build(ticks=ticks_from([0, 100, 200, 300, 500])),
        1,
        "tick_spacing",
    ),
    (
        "tick_axis_unknown: data-tick outside the value axis",
        build(
            ticks=[
                {"tick": "x", "value": 0, "x": 80, "text": "0"},
                {"tick": "x", "value": 100, "x": 280, "text": "100"},
                {"tick": "x", "value": 200, "x": 480, "text": "200"},
                {"tick": "y", "value": 300, "x": 680, "text": "300"},
            ]
        ),
        1,
        "tick_axis_unknown",
    ),
    (
        "transform_forbidden: transform attribute on a dot",
        build(dot_transform={5: "translate(0 8)"}),
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
        build(style=".dot { transform: translateX(4px); }"),
        1,
        "transform_forbidden",
    ),
    (
        "position_forbidden: CSS geometry property in a style block",
        build(style=".dot { cx: 100px; }"),
        1,
        "position_forbidden",
    ),
    (
        "position_forbidden: Level 2 individual property in an inline style",
        build(dot_style={5: "translate: 4px 0"}),
        1,
        "position_forbidden",
    ),
]

SIBLING_CASES = [(gate, BASE) for gate in SIBLING_GATES]


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
    for gate_name, svg in SIBLING_CASES:
        gate = HERE / gate_name
        name = (
            f"sibling treaty (reverse): {gate_name} does not claim the beeswarm figure"
        )
        if not gate.exists():
            failures.append(name)
            print(f"FAIL {name}: {gate} not found")
            continue
        code, output = run_gate(svg, gate)
        if code != 0 or output.strip():
            failures.append(name)
            print(f"FAIL {name}: exit {code}, output: {output.strip()[:400]}")
        else:
            print(f"ok   {name}")
    total = len(CASES) + len(SIBLING_CASES)
    print(f"\n{total - len(failures)}/{total} cases passed")
    if failures:
        print("failed: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
