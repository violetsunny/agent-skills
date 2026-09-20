#!/usr/bin/env python3
"""Both-polarity tests for verify-dumbbell.py.

Contract source: references/type-bar.md line 100: "scripts/test-verify-dumbbell.py
exercises both polarities - including all-zero and zero-touching data, and the
sub-3:1 treatments this replaced."

Every fixture is a synthetic minimal SVG string. The base figure passes every
check (exit 0, no output); each violation case is the base plus exactly one
defect (incidental findings that are a direct consequence of the defect are
tolerated - the expected rule name must appear in the output). Scope-treaty
cases prove foreign-vocabulary files are not claimed, in both directions.

Pinned contract conflict: type-bar.md line 90 gives the dark-skin solid dot as
#f08a59 with an #f5f5f5 stroke; that pair measures 2.27:1 stroke-vs-fill, under
the 3:1 line 72 asks the gate to assert on every skin. The dark-polarity case
therefore expects exit 1 with solid_dot_stroke_fill_contrast - a regression
record of the md conflict, which the gate must not paper over.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-dumbbell.py"
SIBLING_GATES = [
    "verify-slopegraph.py",
    "verify-ridgeline.py",
    "verify-bump.py",
    "verify-bubble.py",
    "verify-beeswarm.py",
    "verify-treemap.py",
]

SKINS = {
    "light": {
        "paper": "#f5f5f5",
        "ink": "#2d3142",
        "muted": "#4f5d75",
        "hollow_fill": "#f5f5f5",
        "hollow_stroke": "#4f5d75",
        "solid_fill": "#eb6c36",
        "solid_stroke": "#2d3142",
        "connector": "rgba(45,49,66,0.55)",
        "grid": "rgba(45,49,66,0.08)",
        "axis": "rgba(45,49,66,0.25)",
    },
    "dark": {
        "paper": "#2d3142",
        "ink": "#f5f5f5",
        "muted": "#bfc0c0",
        "hollow_fill": "#2d3142",
        "hollow_stroke": "#bfc0c0",
        "solid_fill": "#f08a59",
        "solid_stroke": "#f5f5f5",
        "connector": "rgba(245,245,245,0.40)",
        "grid": "rgba(245,245,245,0.08)",
        "axis": "rgba(245,245,245,0.20)",
    },
}
ROW_TABLE = {4: (88, 96), 5: (64, 96), 6: (64, 76), 7: (52, 72), 8: (48, 68)}
MONO = "'Geist Mono', monospace"
SANS = "'Geist', sans-serif"

BASE_ROWS = ((34, 71), (22, 58), (45, 30), (10, 90), (60, 75))
BASE_TICKS = (0, 25, 50, 75, 100)

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
    rounded = round(float(value), 6)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:g}"


def build(rows=BASE_ROWS, ticks=BASE_TICKS, skin="light", ovr=None) -> str:
    ovr = ovr or {}
    s = SKINS[skin]
    floor, ceil = float(ticks[0]), float(ticks[-1])

    def X(v: float) -> int:
        return round(200 + (v - floor) / (ceil - floor) * 760)

    pitch, first_y = ROW_TABLE.get(len(rows), (64, 96))
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">',
        f'<rect x="0" y="0" width="1000" height="500" fill="{s["paper"]}"/>',
    ]
    for t in ticks:
        tv = float(t)
        tov = ovr.get(("tick", tv), {})
        if tov.get("drop"):
            continue
        tx = tov.get("x", X(tv))
        if abs(tv - floor) < 1e-9:
            out.append(
                f'<line x1="{tx}" y1="40" x2="{tx}" y2="420" stroke="{s["axis"]}" stroke-width="1"/>'
            )
        else:
            out.append(
                f'<line x1="{tx}" y1="56" x2="{tx}" y2="408" stroke="{s["grid"]}" stroke-width="0.8"/>'
            )
        out.append(
            f'<text x="{tx}" y="440" fill="{s["muted"]}" font-size="8"'
            f' font-family="{MONO}" text-anchor="middle">{fmt(tv)}</text>'
        )
    if floor < 0 < ceil and not ovr.get(("zeroline",), {}).get("drop"):
        zx = X(0.0)
        out.append(
            f'<line x1="{zx}" y1="40" x2="{zx}" y2="420" stroke="{s["axis"]}" stroke-width="1"/>'
        )
    for i, (ref, focal) in enumerate(rows):
        y = first_y + i * pitch
        xr, xf = X(ref), X(focal)
        xl, xrr = min(xr, xf), max(xr, xf)
        conn = ovr.get(("conn", i), {})
        dot_h = ovr.get(("dot", i, "hollow"), {})
        dot_s = ovr.get(("dot", i, "solid"), {})
        cy = conn.get("y", y)
        conn_el = (
            f'<line x1="{conn.get("x1", xl)}" y1="{cy}" x2="{conn.get("x2", xrr)}"'
            f' y2="{cy}" stroke="{conn.get("stroke", s["connector"])}"'
            f' stroke-width="{conn.get("stroke-width", 1)}"/>'
        )
        hollow_el = None
        if not dot_h.get("drop"):
            hollow_el = (
                f'<circle cx="{dot_h.get("cx", xr)}" cy="{dot_h.get("cy", y)}"'
                f' r="{dot_h.get("r", 6)}" fill="{dot_h.get("fill", s["hollow_fill"])}"'
                f' stroke="{dot_h.get("stroke", s["hollow_stroke"])}"'
                f' stroke-width="{dot_h.get("stroke-width", 1.5)}"/>'
            )
        solid_el = None
        if not dot_s.get("drop"):
            solid_el = (
                f'<circle cx="{dot_s.get("cx", xf)}" cy="{dot_s.get("cy", y)}"'
                f' r="{dot_s.get("r", 6)}" fill="{dot_s.get("fill", s["solid_fill"])}"'
                f' stroke="{dot_s.get("stroke", s["solid_stroke"])}"'
                f' stroke-width="{dot_s.get("stroke-width", 1)}"/>'
            )
        if conn.get("late"):
            out.extend(e for e in (hollow_el, solid_el) if e)
            if not conn.get("drop"):
                out.append(conn_el)
        else:
            if not conn.get("drop"):
                out.append(conn_el)
            out.extend(e for e in (hollow_el, solid_el) if e)
        left_val = ref if xr <= xf else focal
        right_val = focal if xr <= xf else ref
        lab_l = ovr.get(("label", i, "left"), {})
        lab_r = ovr.get(("label", i, "right"), {})
        if not lab_l.get("drop"):
            if xl - 12 < 200:
                lx, lanchor, lbase = xl, "middle", y - 10
            else:
                lx, lanchor, lbase = xl - 12, "end", y + 4
            out.append(
                f'<text x="{lab_l.get("x", lx)}" y="{lab_l.get("y", lbase)}"'
                f' fill="{s["muted"]}" font-size="8" font-family="{MONO}"'
                f' text-anchor="{lab_l.get("anchor", lanchor)}">'
                f"{lab_l.get('text', fmt(left_val))}</text>"
            )
        if not lab_r.get("drop"):
            out.append(
                f'<text x="{lab_r.get("x", xrr + 12)}" y="{lab_r.get("y", y + 4)}"'
                f' fill="{s["muted"]}" font-size="8" font-family="{MONO}"'
                f' text-anchor="{lab_r.get("anchor", "start")}">'
                f"{lab_r.get('text', fmt(right_val))}</text>"
            )
        out.append(
            f'<text x="188" y="{y + 4}" fill="{s["ink"]}" font-size="11"'
            f' font-weight="600" font-family="{SANS}" text-anchor="end">Row {i + 1}</text>'
        )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def run_gate(svg: str) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".svg", delete=False, encoding="utf-8"
    ) as handle:
        handle.write(svg)
        path = handle.name
    proc = subprocess.run(
        [sys.executable, str(GATE), path], capture_output=True, text=True
    )
    Path(path).unlink(missing_ok=True)
    return proc.returncode, proc.stdout


CASES: list[tuple[str, str, int, str | None]] = [
    ("base light dumbbell passes clean", build(), 0, None),
    (
        "dark polarity: line-90 tokens trip stroke-vs-fill (pinned md conflict)",
        build(skin="dark"),
        1,
        "solid_dot_stroke_fill_contrast",
    ),
    (
        "all-zero data takes the floor=0 ceil=1 fallback",
        build(rows=((0, 0), (0, 0), (0, 0), (0, 0)), ticks=(0, 1)),
        0,
        None,
    ),
    (
        "all-zero without the fallback span fails",
        build(rows=((0, 0), (0, 0), (0, 0), (0, 0)), ticks=(0, 100)),
        1,
        "domain_all_zero_fallback",
    ),
    (
        "zero-touching data anchors floor=0, floor label takes the exception",
        build(rows=((0, 50), (10, 60), (20, 70), (30, 80))),
        0,
        None,
    ),
    (
        "negative bracket keeps zero inside with its own line",
        build(rows=((-20, 30), (-40, 10), (-10, 50), (0, 60)), ticks=(-50, 0, 50, 100)),
        0,
        None,
    ),
    (
        "unicode minus in a printed value parses",
        build(
            rows=((-20, 30), (-40, 10), (-10, 50), (0, 60)),
            ticks=(-50, 0, 50, 100),
            ovr={("label", 0, "left"): {"text": "\u221220"}},
        ),
        0,
        None,
    ),
    (
        "bracket without the zero line fails",
        build(
            rows=((-20, 30), (-40, 10), (-10, 50), (0, 60)),
            ticks=(-50, 0, 50, 100),
            ovr={("zeroline",): {"drop": True}},
        ),
        1,
        "zero_line_missing",
    ),
    (
        "truncated domain (floor 40 with lo=45 >= 0) fails",
        build(rows=((45, 71), (50, 68), (55, 80), (60, 90)), ticks=(40, 60, 80, 100)),
        1,
        "domain_truncated",
    ),
    (
        "dot drawn off the shared scale fails",
        build(ovr={("dot", 0, "solid"): {"cx": 743}}),
        1,
        "dot_off_scale",
    ),
    (
        "non-integer cx fails the nearest-integer-pixel rule",
        build(ovr={("dot", 0, "solid"): {"cx": 739.5}}),
        1,
        "pixel_rounding",
    ),
    (
        "sub-3:1 connector (axis 0.25 treatment) fails",
        build(ovr={("conn", 0): {"stroke": "rgba(45,49,66,0.25)"}}),
        1,
        "connector_contrast",
    ),
    (
        "light connector token carried into the dark skin fails",
        build(
            skin="dark",
            ovr={("conn", i): {"stroke": "rgba(45,49,66,0.55)"} for i in range(5)},
        ),
        1,
        "connector_contrast",
    ),
    (
        "sub-3:1 hollow stroke fails",
        build(ovr={("dot", 0, "hollow"): {"stroke": "rgba(45,49,66,0.25)"}}),
        1,
        "hollow_dot_contrast",
    ),
    (
        "solid dot left to the accent stroke (2.86:1) fails",
        build(ovr={("dot", 0, "solid"): {"stroke": "#eb6c36"}}),
        1,
        "solid_dot_stroke_paper_contrast",
    ),
    (
        "ink stroke on a mid-tone fill (1.88:1 vs own fill) fails",
        build(ovr={("dot", 0, "solid"): {"fill": "#555a6e"}}),
        1,
        "solid_dot_stroke_fill_contrast",
    ),
    (
        "two hollow dots collapse the shape encoding",
        build(ovr={("dot", 0, "solid"): {"fill": "#f5f5f5"}}),
        1,
        "dot_pair_style",
    ),
    (
        "connector declared after the dots fails the paint order",
        build(ovr={("conn", 0): {"late": True}}),
        1,
        "connector_paint_order",
    ),
    (
        "row without its connector fails",
        build(ovr={("conn", 0): {"drop": True}}),
        1,
        "connector_missing",
    ),
    (
        "row that lost an endpoint fails",
        build(ovr={("dot", 0, "solid"): {"drop": True}}),
        1,
        "row_endpoint_count",
    ),
    (
        "unlabelled endpoint fails",
        build(ovr={("label", 0, "left"): {"drop": True}}),
        1,
        "value_label_missing",
    ),
    (
        "fewer than two ticks cannot prove the scale finite",
        build(
            ovr={
                ("tick", 25.0): {"drop": True},
                ("tick", 50.0): {"drop": True},
                ("tick", 75.0): {"drop": True},
                ("tick", 100.0): {"drop": True},
            }
        ),
        1,
        "scale_unverifiable",
    ),
    (
        "tick off the fitted line fails",
        build(ovr={("tick", 50.0): {"x": 584}}),
        1,
        "tick_off_scale",
    ),
    ("scope treaty: slopegraph-only file is not claimed", SLOPE_ONLY_SVG, 0, None),
    ("scope treaty: ridgeline-only file is not claimed", RIDGE_ONLY_SVG, 0, None),
    ("scope treaty: bump-only file is not claimed", BUMP_ONLY_SVG, 0, None),
    ("scope treaty: bubble-only file is not claimed", BUBBLE_ONLY_SVG, 0, None),
]

SIBLING_CASES = [(gate, build()) for gate in SIBLING_GATES]


def main() -> int:
    failures = 0
    for name, svg, expect_code, expect_rule in CASES:
        code, out = run_gate(svg)
        if code != expect_code:
            failures += 1
            print(f"FAIL {name}: exit {code}, expected {expect_code}\n{out}")
            continue
        if expect_rule is None:
            if out.strip():
                failures += 1
                print(f"FAIL {name}: expected no findings, got:\n{out}")
                continue
        elif expect_rule not in out:
            failures += 1
            print(f"FAIL {name}: expected rule {expect_rule!r} in output:\n{out}")
            continue
        print(f"ok   {name}")
    for gate_name, svg in SIBLING_CASES:
        gate = HERE / gate_name
        if not gate.exists():
            failures += 1
            print(f"FAIL sibling treaty: {gate_name} is missing")
            continue
        with tempfile.NamedTemporaryFile(
            "w", suffix=".svg", delete=False, encoding="utf-8"
        ) as handle:
            handle.write(svg)
            path = handle.name
        proc = subprocess.run(
            [sys.executable, str(gate), path], capture_output=True, text=True
        )
        Path(path).unlink(missing_ok=True)
        if proc.returncode != 0 or proc.stdout.strip():
            failures += 1
            print(
                f"FAIL sibling treaty (reverse): {gate_name} claims the dumbbell figure"
                f" (exit {proc.returncode}):\n{proc.stdout}"
            )
            continue
        print(
            f"ok   sibling treaty (reverse): {gate_name} does not claim the dumbbell figure"
        )
    total = len(CASES) + len(SIBLING_CASES)
    passed = total - failures
    print(f"\n{passed}/{total} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
