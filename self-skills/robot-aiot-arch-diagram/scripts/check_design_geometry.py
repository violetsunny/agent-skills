#!/usr/bin/env python3
"""Design-system geometry checks for diagram SVGs.

Contract source: references/design-system.md
  - Arrow size standard (§6 Arrow markers): markerWidth = canvas viewBox width x 0.9375%,
    markerHeight = markerWidth x 0.7, markerUnits="userSpaceOnUse"; one size for
    all arrows. Examples: 960 -> 9.0x6.3; 1000 -> 9.4x6.6; 1200 -> 11.2x7.9.
  - Attach-point fan (§6 Mandatory connector rules): N connectors on a box edge of length L attach at
    offsets L*k/(N+1); adjacent attach points >= 12px apart (8px minimum for very
    small boxes); no two connectors may share a single attach point.
  - 4px grid (§7 4px grid): x/y coordinates and node dimensions divisible by 4.
    Exempt per contract: stroke widths, opacity values, 22x22 dot pattern (lives
    in <defs>). Also exempt here, documented deviations: border radius rx/ry
    (allowed set 4/6/8), path data (quarter-arc elbows), text x/y (the contract's
    own node pattern uses off-grid baselines like Y+15), font sizes (canonical
    patterns use 7/9/10/11px, contradicting the {8,...,40} table — surfaced in
    the module docs, not enforced), and label/bridge-mask/legend/decoration roles
    (derived placement follows the 6-10px label-margin rule, not the grid).
  - Complexity budget (§7 Complexity budget): generic per-diagram limits — max 9 nodes,
    12 arrows, 2 accent elements. Type-specific budgets (lanes, entities, ...)
    require diagram-type knowledge and are out of scope.

Node counting and the fan check rely on data-graph-role="node" annotations (the
convention used by validate_svg.py). Without annotations they report SKIP notes
instead of guessing. Accent detection assumes the light editorial palette
(accent coral #eb6c36).

Standard library only. Usage:
    python3 check_design_geometry.py <file.svg>

Exit 0 = no errors (warnings/notes allowed), 1 = errors.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
ACCENT_HEX = "#eb6c36"
GRID = 4.0
MAX_NODES = 9
MAX_ARROWS = 12
MAX_ACCENTS = 2
FAN_GAP = 12.0
FAN_GAP_SMALL = 8.0
SMALL_EDGE = 96.0
ATTACH_TOLERANCE = 3.0
MARKER_RATIO = 0.009375
MARKER_ASPECT = 0.7
MARKER_TOLERANCE = 0.15  # contract examples round to 0.1
EXEMPT_ROLES = {"label", "bridge-mask", "legend", "decoration", "background"}


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def num(el: ET.Element, name: str, default: float | None = None) -> float | None:
    value = el.get(name)
    if value is None:
        return default
    m = NUMBER_RE.match(value.strip())
    return float(m.group(0)) if m else default


def on_grid(value: float) -> bool:
    return abs(value % GRID) < 1e-9 or abs(value % GRID - GRID) < 1e-9


def fmt(value: float) -> str:
    return f"{value:g}"


def walk_visible(root: ET.Element):
    """Yield (element, in_defs, role) for every element; role from data-graph-role."""
    stack = [(root, False, None)]
    while stack:
        el, in_defs, inherited = stack.pop()
        tag = local_name(el.tag)
        role = (el.get("data-graph-role") or "").strip().lower() or inherited
        yield el, in_defs or tag in ("defs", "pattern", "symbol"), role
        for child in reversed(list(el)):
            stack.append((child, in_defs or tag in ("defs", "pattern", "symbol"), role))


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h


def node_boxes(root: ET.Element) -> list[Box]:
    """Boxes of elements annotated data-graph-role='node' (rect itself or first rect in group)."""
    boxes: list[Box] = []
    for el, in_defs, _ in walk_visible(root):
        if in_defs or (el.get("data-graph-role") or "").strip().lower() != "node":
            continue
        candidates = (
            [el]
            if local_name(el.tag) == "rect"
            else [d for d in el.iter() if local_name(d.tag) == "rect"]
        )
        for rect in candidates:
            x, y = num(rect, "x", 0.0), num(rect, "y", 0.0)
            w, h = num(rect, "width"), num(rect, "height")
            if None in (x, y, w, h) or w <= 0 or h <= 0:
                continue
            boxes.append(Box(x, y, w, h))
            break
    return boxes


# ---------- path endpoint parsing ----------

PATH_TOKEN_RE = re.compile(r"([MmLlHhVvAaCcSsQqTtZz])|(" + NUMBER_RE.pattern + r")")


def path_endpoints(d: str) -> list[tuple[float, float]]:
    """First and last on-curve points of a path (command-aware)."""
    tokens: list[str] = [m.group(0) for m in PATH_TOKEN_RE.finditer(d)]
    start: tuple[float, float] | None = None
    cur: tuple[float, float] | None = None
    i = 0
    cmd = ""
    nums: list[float] = []

    def flush():
        nonlocal start, cur, cmd, nums
        if not cmd or not nums:
            nums = []
            return
        c = cmd
        if c in ("M", "m"):
            for k in range(0, len(nums) - 1, 2):
                px, py = nums[k], nums[k + 1]
                if c == "m" and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                pt = (px, py)
                if start is None:
                    start = pt
                cur = pt
        elif c in ("L", "l"):
            for k in range(0, len(nums) - 1, 2):
                px, py = nums[k], nums[k + 1]
                if c == "l" and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                cur = (px, py)
        elif c in ("H", "h") and cur is not None:
            for v in nums:
                cur = (cur[0] + v if c == "h" else v, cur[1])
        elif c in ("V", "v") and cur is not None:
            for v in nums:
                cur = (cur[0], cur[1] + v if c == "v" else v)
        elif c in ("A", "a"):
            for k in range(5, len(nums) - 1, 7):
                px, py = nums[k], nums[k + 1]
                if c == "a" and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                cur = (px, py)
        elif c in ("C", "c"):
            for k in range(4, len(nums), 6):
                px, py = nums[k], nums[k + 1]
                if c == "c" and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                cur = (px, py)
        elif c in ("S", "s", "Q", "q"):
            step = 4 if c in ("S", "s") else 4
            for k in range(step - 2, len(nums), step):
                px, py = nums[k], nums[k + 1]
                if c in ("s", "q") and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                cur = (px, py)
        elif c in ("T", "t"):
            for k in range(0, len(nums) - 1, 2):
                px, py = nums[k], nums[k + 1]
                if c == "t" and cur is not None:
                    px, py = cur[0] + px, cur[1] + py
                cur = (px, py)
        elif c in ("Z", "z"):
            cur = start
        nums = []

    while i < len(tokens):
        tok = tokens[i]
        if re.match(r"[A-Za-z]", tok):
            flush()
            cmd = tok
        else:
            nums.append(float(tok))
        i += 1
    flush()
    points = [p for p in (start, cur) if p is not None]
    return points


def connector_endpoints(root: ET.Element) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for el, in_defs, role in walk_visible(root):
        if in_defs or role in EXEMPT_ROLES:
            continue
        tag = local_name(el.tag)
        is_connector = (
            bool(el.get("marker-end") or el.get("marker-start")) or role == "edge"
        )
        if not is_connector:
            continue
        if tag == "line":
            for attr in (("x1", "y1"), ("x2", "y2")):
                x, y = num(el, attr[0], 0.0), num(el, attr[1], 0.0)
                points.append((x, y))
        elif tag in ("path", "polyline", "polygon"):
            if tag == "path":
                points.extend(path_endpoints(el.get("d", "")))
            else:
                nums = [float(n) for n in NUMBER_RE.findall(el.get("points", ""))]
                if len(nums) >= 4:
                    points.append((nums[0], nums[1]))
                    points.append((nums[-2], nums[-1]))
    return points


# ---------- checks ----------


def check_grid(root: ET.Element) -> tuple[list[str], list[str], list[str]]:
    errors, warnings, notes = [], [], []
    for el, in_defs, role in walk_visible(root):
        if in_defs or role in EXEMPT_ROLES:
            continue
        tag = local_name(el.tag)
        ident = el.get("id") or el.get("data-node-id") or "-"
        if tag == "rect":
            for attr in ("x", "y", "width", "height"):
                v = num(el, attr)
                if v is not None and not on_grid(v):
                    errors.append(
                        f"grid: <rect id={ident!r}> {attr}={fmt(v)} not divisible by 4"
                    )
        elif tag == "line":
            for attr in ("x1", "y1", "x2", "y2"):
                v = num(el, attr)
                if v is not None and not on_grid(v):
                    errors.append(
                        f"grid: <line id={ident!r}> {attr}={fmt(v)} not divisible by 4"
                    )
        elif tag in ("circle", "ellipse"):
            for attr in ("cx", "cy"):
                v = num(el, attr)
                if v is not None and not on_grid(v):
                    warnings.append(
                        f"grid: <{tag} id={ident!r}> {attr}={fmt(v)} off 4px grid "
                        f"(badge centers may legitimately be off-grid)"
                    )
    return errors, warnings, notes


def check_budget(root: ET.Element) -> tuple[list[str], list[str], list[str]]:
    errors, warnings, notes = [], [], []
    node_count = sum(
        1
        for el, in_defs, _ in walk_visible(root)
        if not in_defs and (el.get("data-graph-role") or "").strip().lower() == "node"
    )
    arrow_count = 0
    accent_count = 0
    for el, in_defs, role in walk_visible(root):
        if in_defs or role in EXEMPT_ROLES:
            continue
        if el.get("marker-end") or el.get("marker-start") or role == "edge":
            arrow_count += 1
        for prop in ("fill", "stroke"):
            value = (el.get(prop) or "").strip().lower()
            if value == ACCENT_HEX:
                accent_count += 1
                break

    if node_count == 0:
        notes.append(
            "budget: no data-graph-role='node' annotations — node budget and fan checks skipped"
        )
    elif node_count > MAX_NODES:
        errors.append(
            f"budget: {node_count} nodes > max {MAX_NODES} (split into overview + detail)"
        )
    if arrow_count > MAX_ARROWS:
        errors.append(f"budget: {arrow_count} arrows > max {MAX_ARROWS}")
    if accent_count > MAX_ACCENTS:
        errors.append(
            f"budget: {accent_count} accent ({ACCENT_HEX}) elements > max {MAX_ACCENTS}"
        )
    elif accent_count == 0:
        notes.append(
            f"budget: no {ACCENT_HEX} accent usage detected (detection assumes light editorial palette)"
        )
    notes.append(
        f"budget: nodes={node_count} arrows={arrow_count} accents={accent_count}"
    )
    return errors, warnings, notes


def point_on_edge(px: float, py: float, box: Box):
    """Return (side, offset) if the point lies on one of the box edges, else None."""
    tol = ATTACH_TOLERANCE
    if abs(py - box.y) <= tol and box.x - tol <= px <= box.right + tol:
        return "top", px - box.x
    if abs(py - box.bottom) <= tol and box.x - tol <= px <= box.right + tol:
        return "bottom", px - box.x
    if abs(px - box.x) <= tol and box.y - tol <= py <= box.bottom + tol:
        return "left", py - box.y
    if abs(px - box.right) <= tol and box.y - tol <= py <= box.bottom + tol:
        return "right", py - box.y
    return None


def check_fan(root: ET.Element) -> tuple[list[str], list[str], list[str]]:
    errors, warnings, notes = [], [], []
    boxes = node_boxes(root)
    if not boxes:
        notes.append("fan: no annotated node boxes — attach-point fan check skipped")
        return errors, warnings, notes
    endpoints = connector_endpoints(root)
    if not endpoints:
        notes.append("fan: no connectors with markers found — nothing to check")
        return errors, warnings, notes

    groups: dict[tuple[int, str], list[float]] = {}
    for px, py in endpoints:
        for idx, box in enumerate(boxes):
            hit = point_on_edge(px, py, box)
            if hit:
                side, offset = hit
                groups.setdefault((idx, side), []).append(offset)
                break

    for (idx, side), offsets in sorted(groups.items()):
        box = boxes[idx]
        length = box.w if side in ("top", "bottom") else box.h
        n = len(offsets)
        if n < 2:
            continue
        label = f"node#{idx + 1} {side} edge (L={fmt(length)})"
        ordered = sorted(offsets)
        for a, b in zip(ordered, ordered[1:], strict=False):
            if b - a < 1.0:
                errors.append(
                    f"fan: {label}: two connectors share one attach point (offset {fmt(a)})"
                )
        min_gap = FAN_GAP_SMALL if length < SMALL_EDGE else FAN_GAP
        for a, b in zip(ordered, ordered[1:], strict=False):
            if 1.0 <= b - a < min_gap:
                errors.append(
                    f"fan: {label}: attach points {fmt(b - a)}px apart < {fmt(min_gap)}px minimum"
                )
        tolerance = max(2.0, length * 0.05)
        ideal = [length * k / (n + 1) for k in range(1, n + 1)]
        deviation = max(abs(o - i) for o, i in zip(ordered, ideal, strict=False))
        if deviation > tolerance:
            warnings.append(
                f"fan: {label}: attach offsets {[fmt(o) for o in ordered]} deviate "
                f"{fmt(deviation)}px from ideal L*k/(N+1) {[fmt(i) for i in ideal]}"
            )
    return errors, warnings, notes


def check_markers(root: ET.Element) -> tuple[list[str], list[str], list[str]]:
    errors, warnings, notes = [], [], []
    vb = [float(n) for n in NUMBER_RE.findall(root.get("viewBox", ""))]
    if len(vb) != 4 or vb[2] <= 0:
        notes.append("markers: missing viewBox width — arrow size standard not checked")
        return errors, warnings, notes
    expected_w = vb[2] * MARKER_RATIO
    expected_h = expected_w * MARKER_ASPECT

    checked = 0
    for el in root.iter():
        if local_name(el.tag) != "marker":
            continue
        ident = el.get("id", "-")
        children = {local_name(c.tag) for c in el.iter() if c is not el}
        if "circle" in children and not children & {"polygon", "path"}:
            notes.append(
                f"markers: #{ident} is a dot marker — arrow size standard not applied"
            )
            continue
        checked += 1
        units = el.get("markerUnits")
        if units != "userSpaceOnUse":
            errors.append(
                f"markers: #{ident} markerUnits={units!r} — must be 'userSpaceOnUse' "
                f"so arrows never scale with stroke-width"
            )
        mw = num(el, "markerWidth")
        mh = num(el, "markerHeight")
        if mw is None:
            errors.append(
                f"markers: #{ident} missing markerWidth — expected {expected_w:.1f} "
                f"(viewBox width {fmt(vb[2])} x 0.9375%)"
            )
        elif abs(mw - expected_w) > MARKER_TOLERANCE:
            errors.append(
                f"markers: #{ident} markerWidth={fmt(mw)} — expected {expected_w:.1f} "
                f"(viewBox width {fmt(vb[2])} x 0.9375%, tolerance {MARKER_TOLERANCE})"
            )
        if mh is None:
            errors.append(
                f"markers: #{ident} missing markerHeight — expected {expected_h:.1f}"
            )
        elif mw is not None and abs(mh - mw * MARKER_ASPECT) > MARKER_TOLERANCE:
            errors.append(
                f"markers: #{ident} markerHeight={fmt(mh)} — expected {mw * MARKER_ASPECT:.1f} "
                f"(markerWidth x 0.7)"
            )
    if checked == 0 and not notes:
        notes.append("markers: no <marker> definitions found")
    return errors, warnings, notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Design-system geometry checks: 4px grid, complexity budget, "
        "attach-point fan, arrow size standard."
    )
    parser.add_argument("svg_file", type=Path)
    args = parser.parse_args()

    try:
        root = ET.parse(args.svg_file).getroot()
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR cannot parse {args.svg_file}: {exc}")
        return 1
    if local_name(root.tag) != "svg":
        print(f"ERROR root element is <{local_name(root.tag)}>, expected <svg>")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    for check in (check_grid, check_budget, check_fan, check_markers):
        e, w, n = check(root)
        errors += e
        warnings += w
        notes += n

    for item in notes:
        print(f"NOTE  {item}")
    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
