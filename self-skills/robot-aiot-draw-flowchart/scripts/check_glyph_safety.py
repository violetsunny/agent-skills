#!/usr/bin/env python3
"""SVG text glyph safety check (CairoSVG PNG export).

Contract source: references/svg-layout-best-practices.md §SVG 文本字形安全
(CairoSVG 导出) — section present on both skill sides; located by
section name, not line number. CairoSVG + fontconfig
on macOS cannot resolve system CJK font names for certain symbol blocks, so
these characters render as tofu boxes in exported PNGs: ≈ × → ① ② ③ … and
their Unicode neighbours (arrows U+2190-21FF, math operators U+2200-22FF,
enclosed alphanumerics U+2460-24FF).

Safe set: ordinary CJK / Latin letters / digits, ASCII punctuation, and
—— 、，。（）【】：+ / · “” (located by the §SVG 文本字形安全 section name).

Scope: SVG <text> content only. HTML page text is exempt (browsers fall back
per glyph); this rule binds SVG text and PNGs exported via CairoSVG.

Standard library only. Usage:
    python3 check_glyph_safety.py <file.svg>

Exit 0 = no errors (warnings allowed), 1 = errors.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

# Contract-named glyphs and their families -> replacement wording (ERROR tier).
DANGEROUS_CHARS = {
    "\u2192": "演进到/导向",  # →
    "\u2190": "来自/回退",  # ←
    "\u2191": "上升/上行",  # ↑
    "\u2193": "下降/下行",  # ↓
    "\u2248": "约",  # ≈
    "\u00d7": "与/对应",  # ×
    "\u00f7": "除以",  # ÷
    "\u2026": "等",  # …
    "\u2264": "不超过",  # ≤
    "\u2265": "至少",  # ≥
    "\u2260": "不等于",  # ≠
}
ERROR_RANGES = (
    (0x2190, 0x21FF, "arrow block", "方向改用文字（如：演进到/导向）"),
    (0x2200, 0x22FF, "math operator block", "数学符号改用文字（如：约/不超过）"),
    (0x2460, 0x24FF, "enclosed alphanumerics", "圈号改用文字（如：问题1/第1项）"),
)
WARN_RANGES = (
    (0x2600, 0x27BF, "symbol/dingbat block", "改用文字或安全标点"),
    (0x1F000, 0x1FAFF, "emoji block", "删除或改用文字"),
    (0xFE00, 0xFE0F, "variation selector", "删除"),
)
WARN_CHARS = {
    "\u2022": "·",  # • -> middle dot (in safe set)
    "\u00b1": "加减",  # ±
    "\u00b0": "度",  # °
}
SAFE_EXTRA = set(
    "\u2014\u2013\u2018\u2019\u201c\u201d\u00b7\u00a0"
)  # — – ‘ ’ “ ” · nbsp
SAFE_RANGES = (
    (0x0020, 0x007E),  # ASCII printable
    (0x00C0, 0x00D6),  # Latin-1 letters (× U+00D7 excluded)
    (0x00D8, 0x00F6),  # Latin-1 letters (÷ U+00F7 excluded)
    (0x00F8, 0x00FF),
    (0x3000, 0x303F),  # CJK punctuation 、。《》【】
    (0x3400, 0x4DBF),  # CJK ext A
    (0x4E00, 0x9FFF),  # CJK unified
    (0xFF00, 0xFFEF),  # fullwidth forms ，（）：
    (0x3040, 0x30FF),  # kana (Japanese labels)
)

TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text\s*>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]*>")
BLANK_RE = re.compile(
    r"<!--.*?-->|<(style|script)\b[^>]*>.*?</\1\s*>", re.DOTALL | re.IGNORECASE
)


def is_safe(ch: str) -> bool:
    cp = ord(ch)
    if ch in SAFE_EXTRA or ch in "\n\t\r":
        return True
    return any(lo <= cp <= hi for lo, hi in SAFE_RANGES)


def classify(ch: str):
    """Return (tier, suggestion) or None if safe."""
    if is_safe(ch):
        return None
    if ch in DANGEROUS_CHARS:
        return "ERROR", f"改用文字：{DANGEROUS_CHARS[ch]}"
    if ch in WARN_CHARS:
        return "WARN", f"改用：{WARN_CHARS[ch]}"
    cp = ord(ch)
    for lo, hi, name, fix in ERROR_RANGES:
        if lo <= cp <= hi:
            return "ERROR", f"{name}，CairoSVG 渲染为豆腐块 — {fix}"
    for lo, hi, name, fix in WARN_RANGES:
        if lo <= cp <= hi:
            return "WARN", f"{name} — {fix}"
    return "WARN", "不在安全字形集内 — 确认渲染器覆盖或改用文字"


def scan(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read {path}: {exc}"], warnings

    # blank out comments/style/script, preserving newlines for line numbers
    blanked = BLANK_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw)

    seen = set()
    text_blocks = 0
    for m in TEXT_RE.finditer(blanked):
        text_blocks += 1
        line = blanked.count("\n", 0, m.start()) + 1
        content = html.unescape(TAG_RE.sub("", m.group(1)))
        context = content.strip()
        if len(context) > 40:
            context = context[:40] + "..."
        for ch in content:
            verdict = classify(ch)
            if verdict is None:
                continue
            tier, fix = verdict
            key = (line, ch)
            if key in seen:
                continue
            seen.add(key)
            msg = f'line {line}: {ch!r} (U+{ord(ch):04X}) in <text> "{context}" — {fix}'
            (errors if tier == "ERROR" else warnings).append(msg)

    if text_blocks == 0:
        warnings.append("no <text> elements found — nothing to inspect")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag CairoSVG-tofu glyphs in SVG <text> (≈ × → ① … families) and suggest replacements."
    )
    parser.add_argument("svg_file", type=Path)
    args = parser.parse_args()

    errors, warnings = scan(args.svg_file)
    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
