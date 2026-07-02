#!/usr/bin/env python3
"""Platform-agnostic validator for stock-replay-workbench.

Runs filesystem, frontmatter, JSON, and reference consistency checks without
depending on any host-specific skill trigger command.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"

REQUIRED_FILES = [
    "SKILL.md",
    "references/capability-registry.md",
    "references/query-contracts.md",
    "references/source-playbook.md",
    "references/screening-playbook.md",
    "references/replay-template.md",
    "references/validation-playbook.md",
    "references/manual-review-template.md",
    "scripts/render_replay_markdown.py",
    "scripts/stock_replay_cli.py",
    "evals/evals.json",
    "evals/trigger-eval-set.json",
]

CORE_LIB_FILES = [
    "scripts/lib/__init__.py",
    "scripts/lib/common.py",
    "scripts/lib/quote.py",
    "scripts/lib/market.py",
    "scripts/lib/sector.py",
    "scripts/lib/flow.py",
    "scripts/lib/events.py",
    "scripts/lib/fundamental.py",
    "scripts/lib/bond.py",
    "scripts/lib/replay_builder.py",
]

EXPECTED_TRIGGER_TERMS = [
    "盘后复盘",
    "收盘简报",
    "主线题材",
    "强势股/观察池",
    "个股为何走强",
    "题材与资金联动",
    "龙虎榜/公告/研报/财务交叉分析",
]

REQUIRED_BODY_SNIPPETS = [
    "行情、资金、事件、板块、财务、衍生资产",
    "事实、信号、判断、风险",
    "东财只承担“别处拿不到的字段”",
]


def fail(message: str) -> dict[str, str | bool]:
    return {"status": "fail", "message": message, "passed": False}


def ok(message: str) -> dict[str, str | bool]:
    return {"status": "pass", "message": message, "passed": True}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("No valid YAML frontmatter found")

    frontmatter = {}
    for line in match.group(1).splitlines():
        # Skip blank lines and indented continuation lines (multi-line YAML values)
        if not line or line[0] == " " or line[0] == "\t":
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def check_required_files() -> list[dict[str, str | bool]]:
    missing = [item for item in REQUIRED_FILES if not (ROOT / item).exists()]
    if missing:
        return [fail(f"Missing required files: {', '.join(missing)}")]
    return [ok("Required files exist")]


def check_frontmatter() -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    text = SKILL_MD.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        return [fail(str(exc))]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        results.append(fail("Frontmatter missing name"))
    elif not re.fullmatch(r"[a-z0-9-]+", name):
        results.append(fail(f"Frontmatter name is not kebab-case: {name}"))
    else:
        results.append(ok(f"Frontmatter name is valid: {name}"))

    if not description:
        results.append(fail("Frontmatter missing description"))
    else:
        if not description.startswith("Use when"):
            results.append(fail("Description does not start with 'Use when'"))
        else:
            results.append(ok("Description starts with 'Use when'"))

        if len(description) > 1024:
            results.append(fail(f"Description too long: {len(description)} chars"))
        else:
            results.append(ok(f"Description length OK: {len(description)} chars"))

        missing_terms = [
            term for term in EXPECTED_TRIGGER_TERMS if term not in description
        ]
        if missing_terms:
            results.append(
                fail(f"Description missing trigger terms: {', '.join(missing_terms)}")
            )
        else:
            results.append(ok("Description covers expected trigger terms"))

        forbidden = [
            term
            for term in ("API Key", "Wind", "Choice", "iFinD", "Tushare Pro")
            if term in description
        ]
        if forbidden:
            results.append(
                fail(
                    f"Description includes paid/private dependency terms: {', '.join(forbidden)}"
                )
            )
        else:
            results.append(ok("Description does not promise paid/private dependencies"))

    return results


def check_body_consistency() -> list[dict[str, str | bool]]:
    text = SKILL_MD.read_text(encoding="utf-8")
    missing = [snippet for snippet in REQUIRED_BODY_SNIPPETS if snippet not in text]
    if missing:
        return [
            fail(
                f"SKILL.md body missing expected workflow snippets: {', '.join(missing)}"
            )
        ]
    return [ok("SKILL.md body matches expected workflow positioning")]


def check_evals() -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []

    evals_path = ROOT / "evals" / "evals.json"
    trigger_path = ROOT / "evals" / "trigger-eval-set.json"
    try:
        evals_data = json.loads(evals_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [fail(f"evals.json is unreadable or malformed: {exc}")]
    try:
        trigger_data = json.loads(trigger_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [fail(f"trigger-eval-set.json is unreadable or malformed: {exc}")]

    if evals_data.get("skill_name") != "stock-replay-workbench":
        results.append(
            fail("evals.json skill_name does not match stock-replay-workbench")
        )
    else:
        results.append(ok("evals.json skill_name matches frontmatter name"))

    prompts = evals_data.get("evals", [])
    if len(prompts) < 3:
        results.append(fail("evals.json should contain at least 3 eval cases"))
    else:
        results.append(ok(f"evals.json contains {len(prompts)} eval cases"))

    prompt_text = "\n".join(item.get("prompt", "") for item in prompts)
    for label in ("复盘", "分析", "观察池"):
        if label not in prompt_text:
            results.append(fail(f"evals.json does not clearly cover {label} scenario"))
        else:
            results.append(ok(f"evals.json covers {label} scenario"))

    should_trigger = sum(
        1 for item in trigger_data if item.get("should_trigger") is True
    )
    should_not_trigger = sum(
        1 for item in trigger_data if item.get("should_trigger") is False
    )
    if should_trigger == 0 or should_not_trigger == 0:
        results.append(
            fail("trigger-eval-set.json must include both positive and negative cases")
        )
    else:
        results.append(
            ok(
                f"trigger-eval-set.json has {should_trigger} positive and {should_not_trigger} negative cases"
            )
        )

    return results


def check_script_help() -> list[dict[str, str | bool]]:
    script = ROOT / "scripts" / "render_replay_markdown.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return [
            fail(
                f"render_replay_markdown.py --help failed: {proc.stderr.strip() or proc.stdout.strip()}"
            )
        ]
    output = proc.stdout + proc.stderr
    missing = [flag for flag in ("--input", "--output") if flag not in output]
    if missing:
        return [
            fail(
                f"render_replay_markdown.py --help missing flags: {', '.join(missing)}"
            )
        ]
    return [ok("render_replay_markdown.py --help works and lists required flags")]


def check_cli_structure() -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    cli = ROOT / "scripts" / "stock_replay_cli.py"
    if cli.exists():
        results.append(ok("stock_replay_cli.py exists"))
    else:
        results.append(fail("stock_replay_cli.py is missing"))

    missing_libs = [item for item in CORE_LIB_FILES if not (ROOT / item).exists()]
    if missing_libs:
        results.append(fail(f"Missing core lib modules: {', '.join(missing_libs)}"))
    else:
        results.append(ok("Core lib modules exist"))
    return results


def check_cli_help() -> list[dict[str, str | bool]]:
    cli = ROOT / "scripts" / "stock_replay_cli.py"
    if not cli.exists():
        return [fail("stock_replay_cli.py is missing — skipping CLI help checks")]
    checks = [
        ([sys.executable, str(cli), "--help"], "stock_replay_cli.py --help works"),
        (
            [sys.executable, str(cli), "quote-realtime", "--help"],
            "quote-realtime --help works",
        ),
        (
            [sys.executable, str(cli), "market-snapshot", "--help"],
            "market-snapshot --help works",
        ),
        ([sys.executable, str(cli), "news", "--help"], "news --help works"),
        (
            [sys.executable, str(cli), "sentiment-heat", "--help"],
            "sentiment-heat --help works",
        ),
        (
            [sys.executable, str(cli), "render-replay", "--help"],
            "render-replay --help works",
        ),
        (
            [sys.executable, str(cli), "build-replay", "--help"],
            "build-replay --help works",
        ),
    ]
    results: list[dict[str, str | bool]] = []
    for command, label in checks:
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            results.append(
                fail(f"{label}: {proc.stderr.strip() or proc.stdout.strip()}")
            )
        else:
            results.append(ok(label))
    return results


def run_checks() -> tuple[bool, list[dict[str, str | bool]]]:
    checks = [
        check_required_files,
        check_frontmatter,
        check_body_consistency,
        check_evals,
        check_cli_structure,
        check_cli_help,
        check_script_help,
    ]

    results: list[dict[str, str | bool]] = []
    failed = False
    for check in checks:
        check_results = check()
        results.extend(check_results)
        failed = failed or any(not bool(item["passed"]) for item in check_results)
    return failed, results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate stock-replay-workbench")
    parser.add_argument(
        "--json", action="store_true", help="Output validation result as JSON"
    )
    args = parser.parse_args()

    failed, results = run_checks()

    summary = "FAILED" if failed else "PASSED"
    if args.json:
        payload = {
            "summary": {
                "status": summary.lower(),
                "passed": not failed,
                "total": len(results),
                "failed": sum(1 for item in results if not bool(item["passed"])),
                "passed_checks": sum(1 for item in results if bool(item["passed"])),
            },
            "results": results,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Validation {summary}")
        for item in results:
            prefix = "PASS" if item["passed"] else "FAIL"
            print(f"{prefix}: {item['message']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
