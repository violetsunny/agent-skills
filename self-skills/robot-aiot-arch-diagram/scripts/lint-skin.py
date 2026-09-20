#!/usr/bin/env python3
"""Repository skin linter for generated diagram HTML files.

Contract sources:
- references/animation.md: "The skin linter rejects modified or additional
  controllers, even when they carry data-diagram-controls."
- references/doctor.md check 3: `scripts/lint-skin.py` is a maintainer-checkout
  gate that must exist in the repository.
- scripts/self_check.py docstring: lint-skin.py is the repository authority for
  the canonical motion controller, external requests, and the accessibility
  contract; self_check.py ships a distilled subset of it.

Scope (skin = single-file safety + accessible SVG naming + controller
identity). Motion-budget and step-structure checks belong to verify-motion.py.

Assumptions:
- CSS loader checks (@import / url() / image-set / remote references) are
  implemented here directly rather than delegated to self_check, so this gate
  behaves identically on every side of the repository regardless of which
  distilled subset the shipped self_check.py carries.
- The canonical controller is the single closed <script> body of
  assets/template-motion.html, resolved relative to this skill installation.

Usage:
    python3 lint-skin.py FILE.html [FILE.html ...]

Exit codes: 0 all files clean, 1 at least one finding.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import self_check  # noqa: E402

CSS_ESCAPE_RE = re.compile(r"\\(?:([0-9a-fA-F]{1,6})[ \t\r\n\f]?|(.))", re.DOTALL)
CSS_IMPORT_RE = re.compile(r"@import\b", re.IGNORECASE)
CSS_URL_RE = re.compile(r"url\(\s*([^)]+?)\s*\)", re.IGNORECASE)
CSS_IMAGE_SET_RE = re.compile(r"(?:-webkit-)?image-set\s*\(", re.IGNORECASE)
CSS_REMOTE_RE = re.compile(r"(?:https?:)?//", re.IGNORECASE)


def normalize_css_escapes(source: str) -> str:
    source = source.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n")

    def replace(match: re.Match[str]) -> str:
        if match.group(1) is None:
            escaped = match.group(2)
            return "" if escaped == "\n" else escaped
        codepoint = int(match.group(1), 16)
        if codepoint == 0 or codepoint > 0x10FFFF:
            return "\N{REPLACEMENT CHARACTER}"
        return chr(codepoint)

    return CSS_ESCAPE_RE.sub(replace, source)


def css_loader_errors(parser: self_check.DiagramParser) -> list[str]:
    # Fail closed on every CSS loader syntax, mirroring self_check.py.
    css_attributes = getattr(parser, "css_attributes", [])
    source = normalize_css_escapes("\n".join(parser.styles + list(css_attributes)))
    errors: list[str] = []
    found_loader = False
    if CSS_IMPORT_RE.search(source):
        errors.append("CSS @import is not allowed")
        found_loader = True
    for match in CSS_URL_RE.finditer(source):
        value = match.group(1).strip().strip("'\"").strip()
        if not value.startswith("#"):
            errors.append("non-fragment CSS url() is not allowed")
            found_loader = True
    if CSS_IMAGE_SET_RE.search(source):
        errors.append("CSS image-set() is not allowed")
        found_loader = True
    if CSS_REMOTE_RE.search(source) and not found_loader:
        errors.append("remote reference in CSS is not allowed")
    return errors


def lint_parser(parser: self_check.DiagramParser) -> list[str]:
    errors: list[str] = list(parser.unsafe)
    errors.extend(css_loader_errors(parser))
    for tag, rel, value in parser.references:
        finding = self_check.reference_error(tag, rel, value)
        if finding:
            errors.append(finding)
    self_check.check_svgs(parser, errors)
    self_check.check_scripts(parser, errors)
    return errors


def lint_source(source: str) -> list[str]:
    return lint_parser(self_check.parsed_document(source))


def lint(path: Path) -> list[str]:
    return lint_source(path.read_text(encoding="utf-8"))


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argument_parser.add_argument("files", nargs="+", type=Path)
    args = argument_parser.parse_args()
    failed = False
    for path in args.files:
        try:
            errors = lint(path)
        except (OSError, UnicodeError, RuntimeError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
