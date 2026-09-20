#!/usr/bin/env python3
"""Adversarial tests for verify-motion.py.

Contract source — references/animation.md: "Its adversarial tests mutate the
canonical template to prove each failure is rejected."

Bipolar fixtures:
- Positive pole: assets/template-motion.html must pass verify-motion.py with
  zero findings.
- Negative pole: every mutation below targets one named verifier check from
  animation.md and must produce a finding matching the expected substring.

Runs with the Python standard library only:
    python3 test-verify-motion.py

Exit codes: 0 all cases green, 1 any case failed.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE = SKILL_DIR / "assets" / "template-motion.html"


def _load_verify_motion():
    spec = importlib.util.spec_from_file_location(
        "verify_motion", SCRIPT_DIR / "verify-motion.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load verify-motion.py from {SCRIPT_DIR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify_motion = _load_verify_motion()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"mutation anchor occurs {text.count(old)} times: {old!r}")
    return text.replace(old, new)


def remove_css_block(text: str, marker: str) -> str:
    start = text.index(marker)
    brace = text.index("{", start)
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[:start] + text[index + 1 :]
    raise AssertionError(f"unbalanced CSS block at {marker!r}")


def duplicate_step5_item(text: str) -> str:
    start = text.index('<g data-motion-item data-step="5"')
    end = text.index("</g>", start) + len("</g>")
    block = text[start:end]
    return text[:end] + ("\n      " + block) * 8 + text[end:]


def crowd_step3(text: str) -> str:
    text = replace_once(
        text, 'data-step="4" aria-label="Step 4:', 'data-step="3" aria-label="Step 4:'
    )
    return replace_once(
        text, 'data-step="5" aria-label="Step 5:', 'data-step="3" aria-label="Step 5:'
    )


def move_status_into_controls(text: str) -> str:
    status = '<p class="sr-only" data-motion-status role="status" aria-live="polite" aria-atomic="true"></p>'
    text = replace_once(text, status, "")
    return replace_once(
        text,
        '<button type="button" data-motion-action="replay">Replay</button>',
        '<button type="button" data-motion-action="replay">Replay</button>\n      '
        + status,
    )


def add_drawn_paths(text: str) -> str:
    extra = (
        '<path pathLength="1" class="draw-path" d="M48 440 H120"/>\n'
        '      <path pathLength="1" class="draw-path" d="M48 456 H120"/>\n    '
    )
    return replace_once(text, "</svg>", extra + "</svg>")


def shorten_loop_cycle(text: str) -> str:
    text = replace_once(text, 'data-motion-mode="step"', 'data-motion-mode="loop"')
    return replace_once(
        text,
        "animation: token-flow 3.2s linear 1 forwards;",
        "animation: token-flow 1.2s linear 1 forwards;",
    )


# (case name, mutation, expected finding substring) — one case per verifier
# check named in animation.md, plus the shared skin/controller checks.
MUTATIONS: list[tuple[str, object, str]] = [
    (
        "mode-declaration-invalid",
        lambda t: replace_once(
            t, 'data-motion-mode="step"', 'data-motion-mode="drift"'
        ),
        "data-motion-mode must be one of",
    ),
    (
        "initial-frame-not-static",
        lambda t: replace_once(
            t,
            'data-step-current="5" data-frame="static"',
            'data-step-current="5" data-frame="end"',
        ),
        "initial data-frame",
    ),
    (
        "steps-not-contiguous",
        lambda t: replace_once(
            t, 'data-step="4" aria-label="Step 4:', 'data-step="7" aria-label="Step 4:'
        ),
        "contiguous",
    ),
    (
        "step-count-mismatch",
        lambda t: replace_once(t, 'data-step-count="5"', 'data-step-count="4"'),
        "contiguous 1..4",
    ),
    ("item-budget-exceeded", duplicate_step5_item, "motion item budget is 12"),
    ("crowded-step", crowd_step3, "no more than two semantic items"),
    (
        "total-over-8s-budget",
        lambda t: replace_once(t, "--motion-total: 3600ms", "--motion-total: 9000ms"),
        "exceeds the 8000ms budget",
    ),
    (
        "total-not-steps-times-hold",
        lambda t: replace_once(t, "--motion-hold: 720ms", "--motion-hold: 600ms"),
        "must equal step count x --motion-hold",
    ),
    (
        "transition-out-of-range",
        lambda t: replace_once(t, "--motion-step: 480ms", "--motion-step: 900ms"),
        "160-600ms",
    ),
    (
        "translation-over-24px",
        lambda t: replace_once(
            t, "transform: translateY(8px);", "transform: translateY(40px);"
        ),
        "exceeds the 24px budget",
    ),
    ("too-many-drawn-paths", add_drawn_paths, "at most 2 drawn paths"),
    ("loop-cycle-under-3s", shorten_loop_cycle, "below the 3s minimum"),
    (
        "svg-naming-order",
        lambda t: replace_once(
            t,
            'aria-labelledby="template-motion-title template-motion-desc"',
            'aria-labelledby="template-motion-desc template-motion-title"',
        ),
        "must name title then desc",
    ),
    (
        "item-hidden-in-source",
        lambda t: replace_once(
            t,
            '<g data-motion-item data-step="1" aria-label="Step 1: Request received">',
            '<g data-motion-item data-step="1" aria-label="Step 1: Request received" style="opacity:0">',
        ),
        "hidden in source",
    ),
    (
        "missing-noscript",
        lambda t: replace_once(
            t,
            "<noscript><p>Animation controls require JavaScript. The complete final diagram is shown above.</p></noscript>",
            "",
        ),
        "needs a <noscript>",
    ),
    (
        "decorative-missing-aria-hidden",
        lambda t: replace_once(
            t,
            'data-motion-decorative aria-hidden="true" focusable="false" pathLength="1"',
            'data-motion-decorative focusable="false" pathLength="1"',
        ),
        "needs aria-hidden=true",
    ),
    (
        "control-set-incomplete",
        lambda t: replace_once(
            t,
            '<button type="button" data-motion-action="next">Next</button>\n      ',
            "",
        ),
        "missing actions: next",
    ),
    (
        "status-inside-controls",
        move_status_into_controls,
        "must sit outside data-motion-controls",
    ),
    (
        "status-missing-aria-live",
        lambda t: replace_once(
            t,
            'data-motion-status role="status" aria-live="polite" aria-atomic="true"',
            'data-motion-status role="status" aria-atomic="true"',
        ),
        "motion status needs role=status",
    ),
    (
        "no-reduced-motion-css",
        lambda t: remove_css_block(t, "@media (prefers-reduced-motion: reduce)"),
        "missing reduced-motion CSS",
    ),
    (
        "no-print-css",
        lambda t: remove_css_block(t, "@media print"),
        "missing print CSS",
    ),
    (
        "controller-modified",
        lambda t: replace_once(
            t,
            "const params = new URLSearchParams(location.search);",
            "const params = new URLSearchParams(String(location.search));",
        ),
        "must exactly match the controller",
    ),
    (
        "additional-controller",
        lambda t: replace_once(
            t, "</body>", "<script data-diagram-controls></script>\n</body>"
        ),
        "at most one script",
    ),
    (
        "motion-root-removed",
        lambda t: replace_once(
            t, "<main data-motion-root data-motion-mode=", "<main data-motion-mode="
        ),
        "expected exactly one data-motion-root",
    ),
]


def run_case(name: str, text: str, expect: str | None) -> tuple[bool, list[str]]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".html", encoding="utf-8", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        errors = verify_motion.verify(temporary)
    finally:
        temporary.unlink(missing_ok=True)
    if expect is None:
        return (errors == [], errors)
    return (any(expect in error for error in errors), errors)


def main() -> int:
    template = TEMPLATE.read_text(encoding="utf-8")
    failures = 0

    passed, errors = run_case("canonical-template", template, None)
    if passed:
        print("[PASS] canonical-template passes with zero findings")
    else:
        failures += 1
        print("[FAIL] canonical-template must pass with zero findings")
        for error in errors:
            print(f"       - {error}")

    for name, mutate, expect in MUTATIONS:
        try:
            mutated = mutate(template)
        except (AssertionError, ValueError) as exc:
            failures += 1
            print(f"[FAIL] {name}: mutation could not be applied ({exc})")
            continue
        passed, errors = run_case(name, mutated, expect)
        if passed:
            print(f"[PASS] {name}: rejected with {expect!r}")
        else:
            failures += 1
            print(f"[FAIL] {name}: expected a finding containing {expect!r}")
            for error in errors:
                print(f"       - {error}")

    total = len(MUTATIONS) + 1
    print(f"test-verify-motion: {total - failures}/{total} cases green")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
