#!/usr/bin/env python3
"""Verify design-system connector/label geometry rule 6 on a diagram file.

Contract source — references/design-system.md §6 "Mandatory connector rules",
rule 6: "A label mask must not overlap a node drawn after it. ... Because
nodes are painted after labels, a mask that lands partly inside a node is
covered by the node fill and the text renders as a fragment sitting on the
node border. ... A mask fully *inside* a node is a badge chip and is fine; a
mask overlapping a zone container is fine too, since zones are painted first.
From a repository checkout, verify with
`python3 <repo-root>/scripts/verify-geometry.py <file>`."

Input is an .svg file or an .html file containing <svg> blocks. Document
order is paint order, per the design system's z-order convention.

Classification (documented assumptions — the hand-authored design-system
pattern carries no data-graph-role annotations):
- Explicit `data-graph-role` wins: "node" is a node; "container",
  "background", "legend", "decoration", "bridge-mask", "reserved" are zones
  and never participate as nodes or masks.
- Zone/container heuristic: rect with stroke-dasharray, fill none/transparent,
  or covering >=90% of the viewBox in either axis.
- Node heuristic: rect carrying a visible stroke, not zone-like.
- Label-mask heuristic: rect without stroke, opaque fill, height <= 28px
  (the small paper rect the design system puts behind arrow labels), not
  zone-like. A node's own paper mask rect overlaps its styled box exactly, so
  the badge-chip exception absorbs it without pair detection.
- Only nodes painted *after* the mask are checked; a mask fully inside one
  later node is a badge chip and passes. Overlap must exceed 0.5px^2 to count.
- Transforms are honoured via validate_svg.walk's matrix accumulation; <defs>
  content is ignored.

Usage:
    python3 verify-geometry.py FILE.svg|FILE.html [FILE ...]

Exit codes: 0 all files clean, 1 at least one finding.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_svg import (  # noqa: E402
    Bounds,
    ElementContext,
    canvas_size,
    local_name,
    parse_number,
    transformed_bounds,
    walk,
)

SVG_BLOCK_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.IGNORECASE)
ZONE_ROLES = {
    "background",
    "bridge-mask",
    "container",
    "decoration",
    "legend",
    "reserved",
}
MASK_MAX_HEIGHT = 28.0
OVERLAP_EPSILON = 0.5
INSIDE_EPSILON = 0.5


def svg_roots(path: Path) -> tuple[list[ET.Element], list[str]]:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []
    roots: list[ET.Element] = []
    blocks = [text] if path.suffix.lower() == ".svg" else SVG_BLOCK_RE.findall(text)
    if not blocks:
        findings.append(f"{path.name}: no <svg> content found")
    for index, block in enumerate(blocks, 1):
        try:
            roots.append(ET.fromstring(block.strip()))
        except ET.ParseError as exc:
            findings.append(f"{path.name}: svg block {index} does not parse ({exc})")
    return roots, findings


def rect_bounds(context: ElementContext) -> Bounds | None:
    element = context.element
    x = parse_number(element.get("x"), 0.0)
    y = parse_number(element.get("y"), 0.0)
    width = parse_number(element.get("width"), None)
    height = parse_number(element.get("height"), None)
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return transformed_bounds(
        context.matrix,
        ((x, y), (x + width, y), (x + width, y + height), (x, y + height)),
    )


def is_zone_like(
    context: ElementContext, bounds: Bounds, canvas: tuple[float, float]
) -> bool:
    element = context.element
    if context.role in ZONE_ROLES:
        return True
    fill = (element.get("fill") or "").strip().lower()
    if fill in {"none", "transparent"}:
        return True
    if element.get("stroke-dasharray"):
        return True
    canvas_width, canvas_height = canvas
    return (
        canvas_width > 0
        and canvas_height > 0
        and (
            (bounds.right - bounds.left) >= canvas_width * 0.9
            or (bounds.bottom - bounds.top) >= canvas_height * 0.9
        )
    )


def has_visible_stroke(context: ElementContext) -> bool:
    stroke = (context.element.get("stroke") or "").strip().lower()
    return bool(stroke) and stroke != "none"


def classify(
    root: ET.Element,
) -> tuple[list[tuple[int, Bounds]], list[tuple[int, Bounds]]]:
    """Return (label_masks, nodes) as (paint_order, bounds) lists."""
    canvas = canvas_size(root)
    masks: list[tuple[int, Bounds]] = []
    nodes: list[tuple[int, Bounds]] = []
    for order, context in enumerate(walk(root)):
        if context.in_defs or local_name(context.element.tag) != "rect":
            continue
        bounds = rect_bounds(context)
        if bounds is None:
            continue
        explicit = context.role
        if explicit == "node":
            nodes.append((order, bounds))
            continue
        if is_zone_like(context, bounds, canvas):
            continue
        if has_visible_stroke(context) and explicit != "label":
            nodes.append((order, bounds))
            continue
        if (
            not has_visible_stroke(context)
            and (bounds.bottom - bounds.top) <= MASK_MAX_HEIGHT
            and (context.element.get("fill") or "").strip().lower()
            not in {"", "none", "transparent"}
        ):
            masks.append((order, bounds))
    return masks, nodes


def overlap_area(first: Bounds, second: Bounds) -> float:
    width = min(first.right, second.right) - max(first.left, second.left)
    height = min(first.bottom, second.bottom) - max(first.top, second.top)
    return width * height if width > 0 and height > 0 else 0.0


def is_inside(mask: Bounds, node: Bounds) -> bool:
    return (
        mask.left >= node.left - INSIDE_EPSILON
        and mask.top >= node.top - INSIDE_EPSILON
        and mask.right <= node.right + INSIDE_EPSILON
        and mask.bottom <= node.bottom + INSIDE_EPSILON
    )


def describe(bounds: Bounds) -> str:
    return (
        f"rect[x={bounds.left:g} y={bounds.top:g} "
        f"w={bounds.right - bounds.left:g} h={bounds.bottom - bounds.top:g}]"
    )


def verify(path: Path) -> list[str]:
    roots, findings = svg_roots(path)
    for root in roots:
        masks, nodes = classify(root)
        # ponytail: O(masks x nodes) scan; hand-authored diagrams stay small.
        for mask_order, mask in masks:
            for node_order, node in nodes:
                if node_order <= mask_order:
                    continue
                if overlap_area(mask, node) <= OVERLAP_EPSILON:
                    continue
                if is_inside(mask, node):
                    continue  # badge chip — allowed by rule 6
                findings.append(
                    f"label_mask_overlap: {describe(mask)} is overlapped by later node "
                    f"{describe(node)} — the node fill would clip the label text (§6 rule 6)"
                )
    return findings


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argument_parser.add_argument("files", nargs="+", type=Path)
    args = argument_parser.parse_args()
    failed = False
    for path in args.files:
        try:
            findings = verify(path)
        except (OSError, UnicodeError) as exc:
            findings = [str(exc)]
        if findings:
            failed = True
            print(f"FAIL {path}")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
