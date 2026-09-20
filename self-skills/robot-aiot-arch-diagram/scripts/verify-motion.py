#!/usr/bin/env python3
"""Repository motion verifier for animated diagram HTML files.

Contract source — references/animation.md ("Export and verification"):
"The verifier checks mode/state declarations, contiguous steps, motion
budgets, complete SVG naming, no-JS source visibility, decorative
accessibility, the full control set, live status, reduced-motion/print CSS,
keyboard handling, page-hide pause, bounded static/test overrides, immediate
final-step stop, and exact canonical-controller identity."

How each named check is discharged:
- Contiguous steps, no-JS source visibility, decorative accessibility, control
  set, live status, reduced-motion/print CSS, complete SVG naming: delegated to
  self_check.check_motion / the skin linter (same repository directory).
- Keyboard handling, page-hide pause, bounded static/test overrides, immediate
  final-step stop, exact canonical-controller identity: enforced by the
  controller-identity check in lint-skin.py — the canonical controller in
  assets/template-motion.html is the executable implementation contract for all
  of these behaviors, so any deviation is rejected there.
- Mode/state declarations and motion budgets: implemented here on top of the
  shared checks, from animation.md sections "Static-first enhancement contract"
  and "Complexity and deterministic timing":
    * initial data-frame="static" on the motion root;
    * --motion-fast / --motion-step transitions within 160-600ms;
    * --motion-hold within 400-1200ms;
    * --motion-total <= 8000ms, and >= 3000ms for the sanctioned reveal
      autoplay ("3-8s total autoplay");
    * --motion-total == data-step-count x --motion-hold;
    * item translation <= 24px inside [data-motion-item] CSS rules;
    * at most 2 drawn paths (elements carrying pathLength="1");
    * loop-mode flow-token cycle >= 3s.

Assumptions:
- CSS is scanned with a naive brace-matching rule-block reader; nested at-rule
  inner rules are read by their inner selector, which is sufficient for the
  declared motion variables and item/token rules of the canonical skin.
- A file without any data-motion-root is rejected: this gate verifies animated
  diagrams; static diagrams run mode "none" inside a motion-root or need no
  motion verification at all.

Usage:
    python3 verify-motion.py FILE.html [FILE.html ...]

Exit codes: 0 all files pass, 1 at least one finding.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import self_check  # noqa: E402


def _load_skin_linter():
    spec = importlib.util.spec_from_file_location(
        "lint_skin", SCRIPT_DIR / "lint-skin.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load lint-skin.py from {SCRIPT_DIR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


skin_lint = _load_skin_linter()

MOTION_VAR_RE = {
    name: re.compile(rf"--motion-{name}\s*:\s*([-+]?[0-9]*\.?[0-9]+)ms")
    for name in ("fast", "step", "hold", "total")
}
TRANSLATE_PX_RE = re.compile(
    r"translate(?:[XY])?\(\s*(-?[0-9]*\.?[0-9]+)px(?:\s*,\s*(-?[0-9]*\.?[0-9]+)px)?\s*\)"
)
PATH_LENGTH_ONE_RE = re.compile(r"pathLength\s*=\s*[\"']1[\"']", re.IGNORECASE)
ANIMATION_TIME_RE = re.compile(r"(?<![\w.])([0-9]*\.?[0-9]+)(m?s)(?![\w.])")
ASCII_DECIMAL_RE = re.compile(r"^[0-9]+$")


def css_rule_blocks(css: str) -> list[tuple[str, str]]:
    """Return (selector, body) pairs from a naive brace-matching scan."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    blocks: list[tuple[str, str]] = []
    buffer: list[str] = []
    stack: list[str] = []
    body: list[str] = []
    for char in css:
        if char == "{":
            if stack:
                body.append(char)
            stack.append("".join(buffer).strip())
            buffer = []
        elif char == "}":
            if stack:
                selector = stack.pop()
                if stack:
                    body.append("}")
                else:
                    blocks.append((selector, "".join(body)))
                    body = []
            buffer = []
        elif stack:
            body.append(char)
        else:
            buffer.append(char)
    return blocks


def motion_variables(styles: str) -> dict[str, float | None]:
    values: dict[str, float | None] = {}
    for name, pattern in MOTION_VAR_RE.items():
        match = pattern.search(styles)
        values[name] = float(match.group(1)) if match else None
    return values


def budget_errors(parser: self_check.DiagramParser, source: str) -> list[str]:
    errors: list[str] = []
    if not parser.roots:
        errors.append("no data-motion-root found; nothing to verify as animated")
        return errors
    if len(parser.roots) != 1:
        return errors  # self_check.check_motion already reports the count.
    root = parser.roots[0]
    mode = root.get("data-motion-mode", "")

    if root.get("data-frame", "") != "static":
        errors.append(
            'initial data-frame on the motion root must be "static"; '
            f"found {root.get('data-frame', '')!r}"
        )

    styles = "".join(parser.styles)
    variables = motion_variables(styles)
    for name in ("fast", "step", "hold", "total"):
        if variables[name] is None:
            errors.append(f"missing --motion-{name} declaration")

    for name in ("fast", "step"):
        value = variables[name]
        if value is not None and not 160.0 <= value <= 600.0:
            errors.append(
                f"--motion-{name} {value:g}ms is outside the 160-600ms transition budget"
            )
    hold = variables["hold"]
    if hold is not None and not 400.0 <= hold <= 1200.0:
        errors.append(f"--motion-hold {hold:g}ms is outside the 400-1200ms hold budget")
    total = variables["total"]
    if total is not None:
        if total > 8000.0:
            errors.append(f"--motion-total {total:g}ms exceeds the 8000ms budget")
        if mode == "reveal" and total < 3000.0:
            errors.append(
                f"--motion-total {total:g}ms is below the 3000ms reveal autoplay floor"
            )
    raw_count = root.get("data-step-count", "")
    if (
        ASCII_DECIMAL_RE.fullmatch(raw_count)
        and hold is not None
        and total is not None
        and int(raw_count) > 0
        and abs(total - int(raw_count) * hold) > 0.5
    ):
        errors.append(
            f"--motion-total {total:g}ms must equal step count x --motion-hold "
            f"({raw_count} x {hold:g}ms = {int(raw_count) * hold:g}ms)"
        )

    for selector, body in css_rule_blocks(styles):
        if "[data-motion-item]" in selector:
            for match in TRANSLATE_PX_RE.finditer(body):
                for axis in match.groups():
                    if axis is not None and abs(float(axis)) > 24.0:
                        errors.append(
                            f"motion item translation {float(axis):g}px exceeds the 24px budget "
                            f"(rule {selector!r})"
                        )
        if mode == "loop" and "flow-token" in selector:
            animation = re.search(r"animation\s*:\s*([^;]+)", body)
            if animation:
                times = ANIMATION_TIME_RE.findall(animation.group(1))
                if times:
                    value, unit = times[0]
                    seconds = float(value) / 1000.0 if unit == "ms" else float(value)
                    if seconds < 3.0:
                        errors.append(
                            f"loop-mode flow-token cycle {seconds:g}s is below the 3s minimum "
                            f"(rule {selector!r})"
                        )

    drawn_paths = len(PATH_LENGTH_ONE_RE.findall(source))
    if drawn_paths > 2:
        errors.append(
            f"at most 2 drawn paths (pathLength=1) are allowed; found {drawn_paths}"
        )
    return errors


def verify(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    parser = self_check.parsed_document(source)
    errors = skin_lint.lint_parser(parser)
    self_check.check_motion(parser, source, errors)
    errors.extend(budget_errors(parser, source))
    return errors


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argument_parser.add_argument("files", nargs="+", type=Path)
    args = argument_parser.parse_args()
    failed = False
    for path in args.files:
        try:
            errors = verify(path)
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
