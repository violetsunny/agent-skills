#!/usr/bin/env python3
"""Both-polarity tests for verify-waterfall.py.

Contract source: references/type-waterfall.md line 68: "scripts/test-verify-waterfall.py
proves both polarities - the shipped examples pass, and each mutation class above
fails with a named finding." The mutation classes are the six honesty rules
(conservation, bridges span exactly two levels, carries at level/span/value,
every bar prints a signed value, zero bridges dropped, degenerate start) plus the
anti-patterns (floating bar, sign by hue, truncated axis, >1 subtotal) and the
structural/geometry/treatment rules.

Every fixture is a synthetic minimal SVG string. The base figure passes every
check (exit 0, no output); each violation case is the base plus exactly one
defect (incidental findings that are a direct consequence of the defect are
tolerated - the expected rule name must appear in the output). Scope-treaty
cases prove foreign-vocabulary files are not claimed, in both directions.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-waterfall.py"
SIBLING_GATES = [
    "verify-slopegraph.py",
    "verify-ridgeline.py",
    "verify-bump.py",
    "verify-bubble.py",
    "verify-beeswarm.py",
    "verify-treemap.py",
    "verify-dumbbell.py",
]

PLOT_Y0, PLOT_Y1 = 40.0, 420.0
BAR_W, BAR_PITCH, BAR_X0 = 96, 144, 112
MONO = "'Geist Mono', monospace"

SKINS = {
    "light": {
        "paper": "#f5f5f5",
        "ink": "#2d3142",
        "muted": "#4f5d75",
        "accent": "#eb6c36",
        "total_fill": "rgba(45,49,66,0.08)",
        "increase_fill": "rgba(79,93,117,0.15)",
        "focal_fill": "rgba(235,108,54,0.12)",
        "decrease_fill": "#f5f5f5",
        "carry": "rgba(45,49,66,0.55)",
        "grid": "rgba(45,49,66,0.08)",
        "axis": "rgba(45,49,66,0.25)",
    },
    "dark": {
        "paper": "#2d3142",
        "ink": "#f5f5f5",
        "muted": "#bfc0c0",
        "accent": "#f08a59",
        "total_fill": "rgba(245,245,245,0.08)",
        "increase_fill": "rgba(191,192,192,0.15)",
        "focal_fill": "rgba(240,138,89,0.12)",
        "decrease_fill": "#2d3142",
        "carry": "rgba(245,245,245,0.40)",
        "grid": "rgba(245,245,245,0.08)",
        "axis": "rgba(245,245,245,0.20)",
    },
}

BASE_WALK = (
    ("total", 240, "FY25 base"),
    ("delta", 64, "Headcount"),
    ("delta", -38, "Attrition"),
    ("delta", 52, "Expansion"),
    ("total", 318, "FY26 plan"),
)
BASE_TICKS = (0, 100, 200, 300, 400)

SUB_WALK = (
    ("total", 100, "Open"),
    ("delta", 50, "Gain A"),
    ("subtotal", 150, "H1"),
    ("delta", 50, "Gain B"),
    ("total", 200, "Close"),
)
NEG_WALK = (
    ("total", 100, "Open"),
    ("delta", -150, "Loss"),
    ("delta", 200, "Gain"),
    ("total", 150, "Close"),
)
NEG_TICKS = (-100, 0, 100, 200)

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
</svg>
"""
BEESWARM_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<circle data-value="12" data-bin="0" cx="300" cy="300" r="6" fill="rgba(79,93,117,0.35)" stroke="#4f5d75" stroke-width="1"/>
<circle data-value="18" data-bin="0" cx="314" cy="300" r="6" fill="rgba(79,93,117,0.35)" stroke="#4f5d75" stroke-width="1"/>
</svg>
"""
TREEMAP_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<rect data-share="0.6" data-name="Alpha" x="80" y="40" width="500" height="380" fill="rgba(79,93,117,0.15)" stroke="#4f5d75" stroke-width="1"/>
<rect data-share="0.4" data-name="Beta" x="584" y="40" width="376" height="380" fill="rgba(79,93,117,0.30)" stroke="#4f5d75" stroke-width="1"/>
</svg>
"""
DUMBBELL_ONLY_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">
<line x1="300" y1="120" x2="700" y2="120" stroke="rgba(45,49,66,0.55)" stroke-width="1"/>
<circle cx="300" cy="120" r="6" fill="#f5f5f5" stroke="#4f5d75" stroke-width="1.5"/>
<circle cx="700" cy="120" r="6" fill="#eb6c36" stroke="#2d3142" stroke-width="1"/>
</svg>
"""


def fmt(value: float) -> str:
    rounded = round(float(value), 6)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:g}"


def build(walk=BASE_WALK, ticks=BASE_TICKS, skin="light", ovr=None) -> str:
    ovr = ovr or {}
    s = SKINS[skin]
    t0, tm = float(ticks[0]), float(ticks[-1])
    span = tm - t0

    def Y(v: float) -> float:
        return PLOT_Y1 - (v - t0) / span * (PLOT_Y1 - PLOT_Y0)

    # ---- running levels (assume conservation for a self-consistent drawing) ----
    info = []
    running = float(walk[0][1])
    for idx, (role, value, name) in enumerate(walk):
        value = float(value)
        if idx == 0:
            before = after = running
        elif role == "delta":
            before = running
            running = running + value
            after = running
        else:
            before = after = running
            running = value
        info.append(
            {
                "role": role,
                "value": value,
                "name": name,
                "before": before,
                "after": after,
            }
        )

    # ---- bar geometry (final declared attrs after ovr) ----
    geoms = []
    for i, b in enumerate(info):
        if b["role"] == "delta":
            top = max(b["before"], b["after"])
            bot = min(b["before"], b["after"])
            y = round(Y(top))
            bottom = round(Y(bot))
        else:
            y = round(Y(b["before"]))
            bottom = PLOT_Y1
        geom = {
            "x": BAR_X0 + i * BAR_PITCH,
            "y": y,
            "width": BAR_W,
            "height": bottom - y,
        }
        bov = ovr.get(("bar", i), {})
        for k in ("x", "y", "width", "height"):
            if k in bov:
                geom[k] = bov[k]
        geoms.append(geom)

    levels = [lev for b in info for lev in (b["before"], b["after"])]
    lo, hi = min(levels), max(levels)

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500">']
    if not ovr.get(("paper_drop",), False):
        out.append(f'<rect x="0" y="0" width="1000" height="500" fill="{s["paper"]}"/>')

    # ---- gridlines + tick labels ----
    for t in ticks:
        tov = ovr.get(("tick", float(t)), {})
        if tov.get("drop"):
            continue
        gy = tov.get("y", Y(float(t)))
        out.append(
            f'<line x1="80" y1="{fmt(gy)}" x2="960" y2="{fmt(gy)}"'
            f' stroke="{s["grid"]}" stroke-width="0.8"/>'
        )
        out.append(
            f'<text x="72" y="{fmt(gy)}" fill="{s["muted"]}" font-size="8"'
            f' font-family="{MONO}" text-anchor="end">{fmt(float(t))}</text>'
        )

    # ---- zero line (required when the levels bracket zero) ----
    if lo < 0 < hi and not ovr.get(("zeroline",), {}).get("drop"):
        zy = Y(0.0)
        out.append(
            f'<line x1="80" y1="{fmt(zy)}" x2="960" y2="{fmt(zy)}"'
            f' stroke="{s["axis"]}" stroke-width="1"/>'
        )

    # ---- bars + carries + labels ----
    for i, b in enumerate(info):
        g = geoms[i]
        role, value = b["role"], b["value"]
        # paper-mask twin (matches the declared bar's geometry exactly)
        out.append(
            f'<rect x="{fmt(g["x"])}" y="{fmt(g["y"])}" width="{fmt(g["width"])}"'
            f' height="{fmt(g["height"])}" fill="{s["paper"]}"/>'
        )
        # treatment
        focal = ovr.get(("focal", i), False)
        if role in ("total", "subtotal"):
            fill, stroke = s["total_fill"], s["ink"]
        elif focal:
            fill, stroke = s["focal_fill"], s["accent"]
        elif value > 0:
            fill, stroke = s["increase_fill"], s["muted"]
        else:
            fill, stroke = s["decrease_fill"], s["muted"]
        dv = f"{int(value):+d}" if role == "delta" else str(int(value))
        attrs = {
            "fill": fill,
            "stroke": stroke,
            "stroke-width": 1,
            "data-role": role,
            "data-value": dv,
            "data-name": b["name"],
        }
        bov = ovr.get(("bar", i), {})
        for k in (
            "fill",
            "stroke",
            "stroke-width",
            "data-role",
            "data-value",
            "data-name",
        ):
            if k in bov:
                if bov[k] is None:
                    attrs.pop(k, None)
                else:
                    attrs[k] = bov[k]
        attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        out.append(
            f'<rect x="{fmt(g["x"])}" y="{fmt(g["y"])}" width="{fmt(g["width"])}"'
            f' height="{fmt(g["height"])}" {attr_str}/>'
        )
        # value label
        lov = ovr.get(("label", i), {})
        if not lov.get("drop"):
            decrease = role == "delta" and value < 0
            baseline = (g["y"] + g["height"] + 12) if decrease else (g["y"] - 8)
            centre = g["x"] + g["width"] / 2.0
            text = lov.get("text", dv)
            out.append(
                f'<text x="{fmt(lov.get("x", centre))}" y="{fmt(lov.get("y", baseline))}"'
                f' fill="{s["muted"]}" font-size="8" font-family="{MONO}"'
                f' text-anchor="middle">{text}</text>'
            )
        # carry across the gap to the next bar
        if i < len(info) - 1:
            cov = ovr.get(("carry", i), {})
            if not cov.get("drop"):
                level = info[i]["after"]
                cy = cov.get("y1", round(Y(level)))
                cx1 = cov.get("x1", g["x"] + g["width"])
                cx2 = cov.get("x2", geoms[i + 1]["x"])
                cstroke = cov.get("stroke", s["carry"])
                carry_val = cov.get("data-carry", fmt(level))
                line = (
                    f'<line x1="{fmt(cx1)}" y1="{fmt(cy)}" x2="{fmt(cx2)}" y2="{fmt(cy)}"'
                    f' stroke="{cstroke}" stroke-width="1" data-carry="{carry_val}"/>'
                )
                out.append(line)
                if cov.get("dup"):
                    out.append(line)

    er = ovr.get(("extra_rect",))
    if er:
        attr_str = " ".join(f'{k}="{v}"' for k, v in er.items())
        out.append(f"<rect {attr_str}/>")

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
    # ---- pass polarities ----
    ("base light waterfall passes clean", build(), 0, None),
    ("base dark waterfall passes clean", build(skin="dark"), 0, None),
    ("walk with a subtotal passes clean", build(walk=SUB_WALK), 0, None),
    (
        "negative bracket walk passes with its zero line",
        build(walk=NEG_WALK, ticks=NEG_TICKS),
        0,
        None,
    ),
    (
        "one focal bridge passes clean",
        build(ovr={("focal", 1): True}),
        0,
        None,
    ),
    # ---- declarations ----
    (
        "unknown data-role fails",
        build(ovr={("bar", 1): {"data-role": "bridge"}}),
        1,
        "bar_role_invalid",
    ),
    (
        "bar with no data-value fails",
        build(ovr={("bar", 1): {"data-value": None}}),
        1,
        "bar_value_missing",
    ),
    (
        "unparsable data-value fails",
        build(ovr={("bar", 1): {"data-value": "abc"}}),
        1,
        "bar_value_unparsable",
    ),
    (
        "unsigned delta fails",
        build(ovr={("bar", 1): {"data-value": "64"}}),
        1,
        "delta_sign_missing",
    ),
    (
        "signed total fails",
        build(ovr={("bar", 0): {"data-value": "+240"}}),
        1,
        "total_sign_unexpected",
    ),
    (
        "bar with no data-name fails",
        build(ovr={("bar", 1): {"data-name": ""}}),
        1,
        "name_missing",
    ),
    # ---- walk structure ----
    (
        "two-bar walk is under the 3-bar floor",
        build(walk=(("total", 240, "A"), ("total", 240, "B"))),
        1,
        "bar_count",
    ),
    (
        "three totals exceed the exactly-two rule",
        build(
            walk=(
                ("total", 100, "A"),
                ("total", 100, "B"),
                ("total", 100, "C"),
            )
        ),
        1,
        "total_count",
    ),
    (
        "two subtotals exceed the at-most-one rule",
        build(
            walk=(
                ("total", 100, "A"),
                ("subtotal", 100, "B"),
                ("subtotal", 100, "C"),
                ("total", 100, "D"),
            )
        ),
        1,
        "subtotal_count",
    ),
    (
        "first bar not a total breaks the walk order",
        build(ovr={("bar", 0): {"data-role": "delta"}}),
        1,
        "walk_order",
    ),
    (
        "zero start total is a degenerate start",
        build(ovr={("bar", 0): {"data-value": "0"}}),
        1,
        "start_degenerate",
    ),
    (
        "a drawn zero bridge fails",
        build(ovr={("bar", 2): {"data-value": "+0"}}),
        1,
        "zero_bridge",
    ),
    # ---- conservation ----
    (
        "end total that does not reconcile fails",
        build(ovr={("bar", 4): {"data-value": "999"}}),
        1,
        "conservation_end",
    ),
    (
        "subtotal that does not reconcile fails",
        build(walk=SUB_WALK, ovr={("bar", 2): {"data-value": "999"}}),
        1,
        "conservation_subtotal",
    ),
    # ---- shared scale ----
    (
        "fewer than two ticks with an unsound anchor fails closed",
        build(
            walk=NEG_WALK,
            ticks=NEG_TICKS,
            ovr={
                ("tick", -100.0): {"drop": True},
                ("tick", 100.0): {"drop": True},
                ("tick", 200.0): {"drop": True},
            },
        ),
        1,
        "scale_unverifiable",
    ),
    (
        "ticks running the wrong direction fail",
        build(
            ovr={
                ("tick", 0.0): {"y": 40},
                ("tick", 100.0): {"y": 135},
                ("tick", 200.0): {"y": 230},
                ("tick", 300.0): {"y": 325},
                ("tick", 400.0): {"y": 420},
            }
        ),
        1,
        "scale_direction",
    ),
    (
        "a tick off the fitted line fails",
        build(ovr={("tick", 200.0): {"y": 250}}),
        1,
        "tick_off_scale",
    ),
    # ---- domain ----
    (
        "a clipped domain (floor 200 with lo=240 >= 0) fails",
        build(ticks=(200, 250, 300, 350, 400)),
        1,
        "domain_truncated",
    ),
    (
        "bracket without the zero line fails",
        build(
            walk=NEG_WALK,
            ticks=NEG_TICKS,
            ovr={("zeroline",): {"drop": True}},
        ),
        1,
        "zero_line_missing",
    ),
    # ---- geometry ----
    (
        "bar x off the 4px grid fails",
        build(ovr={("bar", 1): {"x": 113}}),
        1,
        "grid_snap",
    ),
    (
        "non-integer bar y fails the pixel-rounding rule",
        build(ovr={("bar", 1): {"y": 131.5}}),
        1,
        "pixel_rounding",
    ),
    (
        "bar spilling past the plot band fails",
        build(ovr={("bar", 1): {"width": 900}}),
        1,
        "bar_out_of_band",
    ),
    (
        "total not anchored at the baseline fails",
        build(ovr={("bar", 0): {"height": 220}}),
        1,
        "total_geometry",
    ),
    (
        "bridge spanning the wrong levels fails",
        build(ovr={("bar", 1): {"height": 50}}),
        1,
        "bridge_geometry",
    ),
    (
        "uneven bar pitch fails",
        build(ovr={("bar", 2): {"x": 404}}),
        1,
        "bar_pitch",
    ),
    (
        "bar under 50% of the pitch fails",
        build(ovr={("bar", i): {"width": 40} for i in range(len(BASE_WALK))}),
        1,
        "bar_width_ratio",
    ),
    # ---- sign treatment ----
    (
        "total without the ink treatment fails",
        build(ovr={("bar", 0): {"fill": "#000000"}}),
        1,
        "total_treatment",
    ),
    (
        "increase without the muted tint fails",
        build(ovr={("bar", 1): {"fill": "#f5f5f5"}}),
        1,
        "sign_treatment_increase",
    ),
    (
        "decrease that is not hollow fails",
        build(ovr={("bar", 2): {"fill": "rgba(79,93,117,0.15)"}}),
        1,
        "sign_treatment_decrease",
    ),
    (
        "focal bridge with the wrong fill fails",
        build(ovr={("bar", 1): {"stroke": "#eb6c36", "fill": "#f5f5f5"}}),
        1,
        "focal_treatment",
    ),
    (
        "two focal bridges fail",
        build(
            ovr={
                ("bar", 1): {"stroke": "#eb6c36"},
                ("bar", 3): {"stroke": "#eb6c36"},
            }
        ),
        1,
        "focal_count",
    ),
    # ---- carries ----
    (
        "a gap with no carry fails",
        build(ovr={("carry", 0): {"drop": True}}),
        1,
        "carry_missing",
    ),
    (
        "a carry at the wrong level fails",
        build(ovr={("carry", 0): {"y1": 200}}),
        1,
        "carry_level",
    ),
    (
        "a carry that does not span its gap fails",
        build(ovr={("carry", 0): {"x1": 220}}),
        1,
        "carry_span",
    ),
    (
        "a carry declaring the wrong total fails",
        build(ovr={("carry", 0): {"data-carry": "999"}}),
        1,
        "carry_value",
    ),
    (
        "two carries in one gap fail",
        build(ovr={("carry", 0): {"dup": True}}),
        1,
        "carry_unmatched",
    ),
    (
        "a sub-3:1 carry fails",
        build(ovr={("carry", 0): {"stroke": "rgba(45,49,66,0.25)"}}),
        1,
        "carry_contrast",
    ),
    # ---- labels ----
    (
        "a bar with no printed value fails",
        build(ovr={("label", 0): {"drop": True}}),
        1,
        "value_label_missing",
    ),
    (
        "a value label off its baseline fails",
        build(ovr={("label", 0): {"y": 150}}),
        1,
        "label_position",
    ),
    (
        "an unsigned delta label fails",
        build(ovr={("label", 1): {"text": "64"}}),
        1,
        "label_sign_missing",
    ),
    (
        "a signed total label fails",
        build(ovr={("label", 0): {"text": "+240"}}),
        1,
        "label_sign_unexpected",
    ),
    # ---- fail closed ----
    (
        "an undeclared rect inside the plot band fails",
        build(
            ovr={
                ("extra_rect",): {
                    "x": 800,
                    "y": 100,
                    "width": 96,
                    "height": 300,
                    "fill": "#4f5d75",
                }
            }
        ),
        1,
        "undeclared_bar",
    ),
    (
        "no paper rect fails closed",
        build(ovr={("paper_drop",): True}),
        1,
        "paper_undetectable",
    ),
    # ---- scope treaties (foreign vocabulary is not claimed) ----
    ("scope treaty: slopegraph-only file is not claimed", SLOPE_ONLY_SVG, 0, None),
    ("scope treaty: ridgeline-only file is not claimed", RIDGE_ONLY_SVG, 0, None),
    ("scope treaty: bump-only file is not claimed", BUMP_ONLY_SVG, 0, None),
    ("scope treaty: bubble-only file is not claimed", BUBBLE_ONLY_SVG, 0, None),
    ("scope treaty: beeswarm-only file is not claimed", BEESWARM_ONLY_SVG, 0, None),
    ("scope treaty: treemap-only file is not claimed", TREEMAP_ONLY_SVG, 0, None),
    ("scope treaty: dumbbell-only file is not claimed", DUMBBELL_ONLY_SVG, 0, None),
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
                f"FAIL sibling treaty (reverse): {gate_name} claims the waterfall figure"
                f" (exit {proc.returncode}):\n{proc.stdout}"
            )
            continue
        print(
            f"ok   sibling treaty (reverse): {gate_name} does not claim the waterfall figure"
        )
    total = len(CASES) + len(SIBLING_CASES)
    passed = total - failures
    print(f"\n{passed}/{total} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
