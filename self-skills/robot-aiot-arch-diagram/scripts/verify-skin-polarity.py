#!/usr/bin/env python3
"""Gate for directional tone claims against the file's own skin.

Contract source: references/type-treemap.md (Legend bullet): "Name that
direction by contrast against the paper - `stronger contrast is larger` -
never by lightness. `darker is larger` is true only on light paper; ship it
in the dark variant and the legend states the opposite of what the reader
sees, because the ramp's lightness inverts with the skin while its opacity
does not. Named by contrast, one sentence serves all three variants and
cannot rot apart. scripts/verify-skin-polarity.py gates this, checking every
directional tone claim against the ramp composited on that file's own paper."

Checks implemented:
- every directional tone claim printed in any <text> ("darker is larger",
  "lighter = smaller", "stronger contrast means bigger", ...) is evaluated
  against the ink ramp composited on that file's own paper; a claim whose
  asserted direction is false on this skin is a finding
- fail closed: a claim exists but no paper rect can be detected -> finding

Scope treaty: this gate's vocabulary is the directional tone claim itself.
A file printing no directional tone claim is not this gate's business:
exit 0 with no findings and no mention of foreign vocabulary. It reads none
of the sibling gates' data-* vocabulary (data-series slopegraph, data-bins
ridgeline, data-ranks bump, data-value beeswarm, data-size bubble,
data-share treemap).

Assumptions (the contract is one sentence; these are pinned here):
- Paper = the first <rect> in document order whose solid parsed fill covers
  at least 50% of the viewBox area (viewBox defaults to 0 0 1000 500).
  Skin classification: relative luminance >= 0.5 is light, below is dark.
- The file's own ramp = rgba() fills on <rect> elements grouped by rgb
  triple; the group with the most distinct alphas wins (tie: higher
  contrast against paper at the group's max alpha); the ramp ends are its
  min and max alpha and its rgb is the ink. With fewer than two distinct
  alphas detectable, fall back to the contract's ramp ends 0.04/0.16 and
  the house ink token for the skin (45,49,66 light / 245,245,245 dark).
- Ramp strength increases with alpha, and the treemap contract binds
  strength to share ("a larger share never carries a weaker opacity"), so
  "<tone> is larger" asserts the ramp strengthens toward <tone>.
- Claim grammar (case-insensitive): tone term, connector (is|=|means|->|
  →), size term. Tone terms: darker/deeper, lighter/fainter, stronger/
  higher/more contrast, weaker/lower/less contrast. Size terms: larger/
  bigger/greater/more vs smaller/littler/fewer/less.
- Compositing is channel-wise in sRGB space, matching the contrast figures
  printed in the contracts (e.g. ink on paper 11.82:1).
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

VOCAB: tuple[str, ...] = ()

CLAIM_RE = re.compile(
    r"\b(darker|lighter|deeper|fainter|stronger\s+contrast|weaker\s+contrast"
    r"|higher\s+contrast|lower\s+contrast|more\s+contrast|less\s+contrast)"
    r"\s*(?:is|=|means|->|\u2192)\s*"
    r"(larger|bigger|greater|smaller|littler|fewer|more|less)\b",
    re.IGNORECASE,
)
DARK_TONE_TERMS = ("darker", "deeper")
LIGHT_TONE_TERMS = ("lighter", "fainter")
POSITIVE_SIZE_TERMS = ("larger", "bigger", "greater", "more")
EPS = 1e-6
DEFAULT_ALPHAS = (0.04, 0.16)
INK_LIGHT = (45.0, 49.0, 66.0)
INK_DARK = (245.0, 245.0, 245.0)
RGBA_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$"
)
HEX6_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
HEX3_RE = re.compile(r"^#([0-9a-fA-F]{3})$")


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


def parse_color(value: str | None) -> tuple[tuple[float, float, float], float] | None:
    if value is None:
        return None
    value = value.strip()
    match = HEX6_RE.match(value)
    if match:
        digits = match.group(1)
        return (
            (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)),
            1.0,
        )
    match = HEX3_RE.match(value)
    if match:
        digits = match.group(1)
        return (
            (
                int(digits[0] * 2, 16),
                int(digits[1] * 2, 16),
                int(digits[2] * 2, 16),
            ),
            1.0,
        )
    match = RGBA_RE.match(value)
    if match:
        alpha = 1.0 if match.group(4) is None else float(match.group(4))
        return (
            (float(match.group(1)), float(match.group(2)), float(match.group(3))),
            alpha,
        )
    return None


def srgb_to_linear(channel: float) -> float:
    c = channel / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    la, lb = luminance(a), luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def composite(
    fg: tuple[float, float, float], alpha: float, bg: tuple[float, float, float]
) -> tuple[float, float, float]:
    return tuple(alpha * f + (1.0 - alpha) * b for f, b in zip(fg, bg))  # type: ignore[return-value]


def viewBox_of(root: ET.Element) -> tuple[float, float, float, float]:
    parts = (root.get("viewBox") or "").replace(",", " ").split()
    if len(parts) == 4:
        values = [parse_float(p) for p in parts]
        if all(v is not None for v in values):
            return tuple(values)  # type: ignore[return-value]
    return (0.0, 0.0, 1000.0, 500.0)


def detect_paper(root: ET.Element) -> tuple[float, float, float] | None:
    _, _, vb_w, vb_h = viewBox_of(root)
    vb_area = vb_w * vb_h
    for el in root.iter():
        if local_name(el.tag) != "rect":
            continue
        color = parse_color(el.get("fill"))
        if color is None or color[1] < 0.999:
            continue
        x = parse_float(el.get("x")) or 0.0
        y = parse_float(el.get("y")) or 0.0
        w = parse_float(el.get("width"))
        h = parse_float(el.get("height"))
        if w is None or h is None:
            continue
        if w * h >= 0.5 * vb_area:
            return color[0]
    return None


def detect_ramp(
    root: ET.Element, paper: tuple[float, float, float], light_skin: bool
) -> tuple[tuple[float, float, float], float, float]:
    groups: dict[tuple[float, float, float], set[float]] = {}
    for el in root.iter():
        if local_name(el.tag) != "rect":
            continue
        color = parse_color(el.get("fill"))
        if color is None or color[1] >= 1.0:
            continue
        groups.setdefault(color[0], set()).add(round(color[1], 6))
    candidates = [(rgb, alphas) for rgb, alphas in groups.items() if len(alphas) >= 2]
    if candidates:
        rgb, alphas = max(
            candidates,
            key=lambda item: (
                len(item[1]),
                contrast(composite(item[0], max(item[1]), paper), paper),
            ),
        )
        return rgb, min(alphas), max(alphas)
    ink = INK_LIGHT if light_skin else INK_DARK
    return ink, DEFAULT_ALPHAS[0], DEFAULT_ALPHAS[1]


def check(root: ET.Element) -> list[str]:
    claims: list[tuple[ET.Element, str, str, str]] = []
    for el in root.iter():
        if local_name(el.tag) != "text":
            continue
        content = text_of(el)
        for match in CLAIM_RE.finditer(content):
            claims.append((el, match.group(1), match.group(2), match.group(0)))
    if not claims:
        return []

    paper = detect_paper(root)
    if paper is None:
        return [
            "paper_undetectable: <svg>: directional tone claims are printed but no paper"
            " rect (solid fill covering >= 50% of the viewBox) was found; the ramp cannot"
            " be composited on the file's own paper"
        ]

    light_skin = luminance(paper) >= 0.5
    skin = "light" if light_skin else "dark"
    ink, alpha_lo, alpha_hi = detect_ramp(root, paper, light_skin)
    color_lo = composite(ink, alpha_lo, paper)
    color_hi = composite(ink, alpha_hi, paper)
    l_lo, l_hi = luminance(color_lo), luminance(color_hi)
    c_lo = contrast(color_lo, paper)
    c_hi = contrast(color_hi, paper)
    hi_darker = l_hi < l_lo - EPS
    hi_lighter = l_hi > l_lo + EPS
    hi_more_contrast = c_hi > c_lo + EPS

    paper_hex = "#{:02x}{:02x}{:02x}".format(*(int(round(c)) for c in paper))
    findings: list[str] = []
    for el, tone, size, matched in claims:
        tone_norm = re.sub(r"\s+", " ", tone.strip().lower())
        if tone_norm in DARK_TONE_TERMS:
            holds = hi_darker
        elif tone_norm in LIGHT_TONE_TERMS:
            holds = hi_lighter
        elif tone_norm.startswith(("stronger", "higher", "more")):
            holds = hi_more_contrast
        else:
            holds = not hi_more_contrast
        positive = size.strip().lower() in POSITIVE_SIZE_TERMS
        if holds == positive:
            continue
        if hi_darker:
            actual = "darker"
        elif hi_lighter:
            actual = "lighter"
        else:
            actual = "unchanged in lightness"
        findings.append(
            f'polarity_claim_false: {describe(el)}: "{matched}" is false on this file\'s'
            f" {skin} paper ({paper_hex}): the ink ramp composites {actual} as it"
            f" strengthens (alpha {alpha_lo:g} -> {alpha_hi:g}, contrast {c_lo:.2f}:1 ->"
            f' {c_hi:.2f}:1); name the direction by contrast, e.g. "stronger contrast is'
            ' larger"'
        )
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify directional tone claims against the file's own skin"
        " (references/type-treemap.md, Legend bullet)."
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
