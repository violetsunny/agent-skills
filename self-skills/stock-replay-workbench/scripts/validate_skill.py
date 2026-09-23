#!/usr/bin/env python3
"""Platform-agnostic validator for stock-replay-workbench.

Runs filesystem, frontmatter, JSON, and reference consistency checks without
depending on any host-specific skill trigger command.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
STOCK_REPLAY_CLI = ROOT / "scripts" / "stock_replay_cli.py"

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
    "evals/core-acceptance-stocks.json",
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
    "scripts/lib/irm.py",
    "scripts/lib/options.py",
    "scripts/lib/replay_builder.py",
]

EXPECTED_TRIGGER_TERMS = [
    "盘后复盘",
    "收盘简报",
    "主线题材",
    "强势股/观察池",
    "个股为何走强",
    "题材与资金联动",
    "龙虎榜/公告/财务交叉分析",
]

REQUIRED_BODY_SNIPPETS = [
    "行情、资金、事件、板块、财务、衍生资产",
    "事实、信号、判断、风险",
    "东财只承担“别处拿不到的字段”",
]

CORE_ACCEPTANCE_SYMBOLS = {
    "601899": "紫金矿业",
    "300124": "汇川技术",
    "002156": "通富微电",
    "300750": "宁德时代",
    "002920": "德赛西威",
    "603986": "兆易创新",
}

REQUIRED_ACCEPTANCE_LAYERS = ["facts", "signals", "judgment", "risks"]

REQUIRED_FORBIDDEN_BEHAVIORS = {
    "fabricated_fields",
    "fabricated_values",
    "undefined_sections",
    "emotional_recommendation",
}

REQUIRED_CASE_SNIPPETS = [
    "## 已确认事实",
    "## 市场信号",
    "## 分析判断",
    "## 风险提示",
    "## 数据来源与缺失说明",
    "数据来源",
    "warning",
]


def _read_path(data: object, path: str) -> object:
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current.get(part)
    return current


def _layer_text(analysis: dict, layer: str) -> str:
    value = analysis.get(layer)
    if not isinstance(value, list):
        return ""
    return "\n".join(str(item) for item in value if str(item).strip())


def _load_core_acceptance_data() -> dict:
    path = ROOT / "evals" / "core-acceptance-stocks.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_stock_replay_cli_module():
    spec = importlib.util.spec_from_file_location(
        "stock_replay_cli_runtime", STOCK_REPLAY_CLI
    )
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _run_stock_diagnose(symbol: str, limit: int) -> dict:
    module = _load_stock_replay_cli_module()
    return module.stock_diagnose(symbol, limit)


def _normalize_text(value: str) -> str:
    return value.replace('"', "“").replace("”", "“").replace("‘", "'").replace("’", "'")


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
    text = _normalize_text(SKILL_MD.read_text(encoding="utf-8"))
    missing = [
        snippet
        for snippet in REQUIRED_BODY_SNIPPETS
        if _normalize_text(snippet) not in text
    ]
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


def check_core_acceptance_standards() -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    path = ROOT / "evals" / "core-acceptance-stocks.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [fail(f"core-acceptance-stocks.json is unreadable or malformed: {exc}")]

    stocks = data.get("stocks")
    if not isinstance(stocks, list):
        return [fail("core-acceptance-stocks.json must contain a 'stocks' list")]

    if len(stocks) != len(CORE_ACCEPTANCE_SYMBOLS):
        results.append(
            fail(
                f"core-acceptance-stocks.json should contain {len(CORE_ACCEPTANCE_SYMBOLS)} stock standards"
            )
        )
    else:
        results.append(ok("core-acceptance-stocks.json contains 6 stock standards"))

    seen_symbols: set[str] = set()
    for entry in stocks:
        if not isinstance(entry, dict):
            results.append(fail("each core acceptance stock entry must be an object"))
            continue
        symbol = str(entry.get("symbol", "")).strip()
        name = str(entry.get("name", "")).strip()
        seen_symbols.add(symbol)
        expected_name = CORE_ACCEPTANCE_SYMBOLS.get(symbol)
        if not expected_name:
            results.append(
                fail(f"unexpected core acceptance symbol: {symbol or '<blank>'}")
            )
            continue
        if name != expected_name:
            results.append(
                fail(
                    f"{symbol} name mismatch: expected {expected_name}, got {name or '<blank>'}"
                )
            )
        else:
            results.append(ok(f"{symbol} name matches expected stock"))

        thesis = str(entry.get("thesis", "")).strip()
        if not thesis:
            results.append(fail(f"{symbol} thesis must not be blank"))
        else:
            results.append(ok(f"{symbol} thesis is defined"))

        layers = entry.get("required_layers") or []
        if layers != REQUIRED_ACCEPTANCE_LAYERS:
            results.append(
                fail(f"{symbol} required_layers must be {REQUIRED_ACCEPTANCE_LAYERS}")
            )
        else:
            results.append(ok(f"{symbol} required_layers enforce four-layer analysis"))

        domains = entry.get("required_data_domains") or []
        if not isinstance(domains, list) or len(domains) < 3:
            results.append(fail(f"{symbol} must require at least 3 data domains"))
        else:
            results.append(ok(f"{symbol} defines data-domain coverage"))

        fields = entry.get("required_fields") or []
        if not isinstance(fields, list) or len(fields) < 2:
            results.append(
                fail(f"{symbol} must define required_fields for data completeness")
            )
        else:
            results.append(ok(f"{symbol} defines required fields"))

        if entry.get("required_source_trace") is not True:
            results.append(
                fail(f"{symbol} must require source trace for analysis chain integrity")
            )
        else:
            results.append(ok(f"{symbol} requires source trace"))

        tags = entry.get("expected_conclusion_tags") or []
        if not isinstance(tags, list) or not tags:
            results.append(fail(f"{symbol} must define expected conclusion tags"))
        else:
            results.append(ok(f"{symbol} defines expected conclusion tags"))

        forbidden = set(entry.get("forbidden_behaviors") or [])
        missing_forbidden = sorted(REQUIRED_FORBIDDEN_BEHAVIORS - forbidden)
        if missing_forbidden:
            results.append(
                fail(
                    f"{symbol} forbidden_behaviors missing: {', '.join(missing_forbidden)}"
                )
            )
        else:
            results.append(
                ok(
                    f"{symbol} forbids fabrication, undefined sections, and emotional recommendation"
                )
            )

        tone = entry.get("tone_constraints") or {}
        if tone.get("must_be_rational") is not True:
            results.append(
                fail(f"{symbol} tone_constraints must enforce 理性 analysis")
            )
        else:
            results.append(ok(f"{symbol} tone_constraints require rational analysis"))
        forbid_words = tone.get("forbid_words") or []
        if not isinstance(forbid_words, list) or not forbid_words:
            results.append(
                fail(
                    f"{symbol} tone_constraints must include forbidden emotional wording"
                )
            )
        else:
            results.append(ok(f"{symbol} tone_constraints define forbidden wording"))

        case_path_value = str(entry.get("markdown_case", "")).strip()
        if not case_path_value:
            results.append(fail(f"{symbol} markdown_case must not be blank"))
            continue
        case_path = ROOT / case_path_value
        if not case_path.exists():
            results.append(fail(f"{symbol} markdown case missing: {case_path_value}"))
            continue
        case_text = case_path.read_text(encoding="utf-8")
        missing_snippets = [
            snippet for snippet in REQUIRED_CASE_SNIPPETS if snippet not in case_text
        ]
        if missing_snippets:
            results.append(
                fail(
                    f"{symbol} markdown case missing required snippets: {', '.join(missing_snippets)}"
                )
            )
        else:
            results.append(
                ok(
                    f"{symbol} markdown case includes layered sections and source/warning notes"
                )
            )

        forbidden_words_in_case = [word for word in forbid_words if word in case_text]
        if forbidden_words_in_case:
            results.append(
                fail(
                    f"{symbol} markdown case contains forbidden emotional wording: {', '.join(forbidden_words_in_case)}"
                )
            )
        else:
            results.append(
                ok(f"{symbol} markdown case tone is rational and non-emotional")
            )

    missing_symbols = [
        f"{symbol} {name}"
        for symbol, name in CORE_ACCEPTANCE_SYMBOLS.items()
        if symbol not in seen_symbols
    ]
    if missing_symbols:
        results.append(
            fail(f"core acceptance stocks missing: {', '.join(missing_symbols)}")
        )
    else:
        results.append(ok("All 6 required core acceptance stocks are covered"))

    return results


def check_stock_diagnose_payload(
    payload: dict, standard: dict
) -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    data = payload.get("data") or {}
    analysis = data.get("analysis") or {}

    for layer in standard.get("required_layers") or []:
        items = analysis.get(layer)
        if not isinstance(items, list) or not items:
            results.append(
                fail(f"stock_diagnose analysis missing required layer: {layer}")
            )
        else:
            results.append(ok(f"stock_diagnose analysis contains layer: {layer}"))

    for field in standard.get("required_fields") or []:
        value = _read_path(data, str(field))
        if value in (None, [], {}):
            results.append(
                fail(f"stock_diagnose payload missing required field: {field}")
            )
        else:
            results.append(
                ok(f"stock_diagnose payload includes required field: {field}")
            )

    layer_expectations = standard.get("layer_expectations") or {}
    for layer, anchors in layer_expectations.items():
        if not isinstance(anchors, list) or not anchors:
            continue
        text = _layer_text(analysis, str(layer))
        missing = [
            str(anchor) for anchor in anchors if str(anchor) and str(anchor) not in text
        ]
        if missing:
            results.append(
                fail(
                    f"stock_diagnose analysis layer expectation missing in {layer}: {', '.join(missing)}"
                )
            )
        else:
            results.append(
                ok(f"stock_diagnose analysis layer expectation satisfied for {layer}")
            )

    domain_expectations = standard.get("domain_expectations") or {}
    for domain in standard.get("required_data_domains") or []:
        paths = domain_expectations.get(str(domain)) or []
        if not isinstance(paths, list) or not paths:
            continue
        matched = [
            str(path)
            for path in paths
            if _read_path(data, str(path)) not in (None, [], {})
        ]
        if not matched:
            results.append(
                fail(
                    f"stock_diagnose domain expectation missing for {domain}: {', '.join(str(path) for path in paths)}"
                )
            )
        else:
            results.append(
                ok(
                    f"stock_diagnose domain expectation satisfied for {domain}: {', '.join(matched)}"
                )
            )

    if standard.get("required_source_trace") is True:
        source_trace = analysis.get("source_trace")
        if not isinstance(source_trace, list) or not source_trace:
            results.append(fail("stock_diagnose analysis must include source trace"))
        elif source_trace != payload.get("source_chain"):
            results.append(
                fail(
                    "stock_diagnose analysis source trace must match payload source_chain"
                )
            )
        else:
            results.append(ok("stock_diagnose analysis includes source trace"))

    tags = [
        str(tag).strip()
        for tag in (analysis.get("conclusion_tags") or [])
        if str(tag).strip()
    ]
    expected_tags = [
        str(tag).strip()
        for tag in (standard.get("expected_conclusion_tags") or [])
        if str(tag).strip()
    ]
    if not tags:
        results.append(fail("stock_diagnose analysis must include conclusion tags"))
    elif expected_tags and not set(expected_tags).issubset(set(tags)):
        results.append(
            fail(
                "stock_diagnose analysis conclusion tags missing: "
                + ", ".join(sorted(set(expected_tags) - set(tags)))
            )
        )
    else:
        results.append(ok("stock_diagnose analysis includes expected conclusion tags"))

    tone = standard.get("tone_constraints") or {}
    if tone.get("must_be_rational") is True and analysis.get("rational") is not True:
        results.append(fail("stock_diagnose analysis must declare 理性 stance"))
    else:
        results.append(ok("stock_diagnose analysis declares rational stance"))

    forbidden_words = [
        str(word).strip()
        for word in (tone.get("forbid_words") or [])
        if str(word).strip()
    ]
    text_parts: list[str] = []
    for layer in ("facts", "signals", "judgment", "risks"):
        value = analysis.get(layer)
        if isinstance(value, list):
            text_parts.extend(str(item) for item in value)
    text = "\n".join(text_parts)
    found = [word for word in forbidden_words if word in text]
    if found:
        results.append(
            fail(
                "stock_diagnose analysis contains forbidden emotional wording: "
                + ", ".join(found)
            )
        )
    else:
        results.append(ok("stock_diagnose analysis tone is non-emotional"))

    return results


def check_core_acceptance_runtime(limit: int = 5) -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    try:
        data = _load_core_acceptance_data()
    except (json.JSONDecodeError, OSError) as exc:
        return [fail(f"core acceptance runtime load failed: {exc}")]

    stocks = data.get("stocks")
    if not isinstance(stocks, list):
        return [fail("core acceptance runtime requires a 'stocks' list")]

    for entry in stocks:
        if not isinstance(entry, dict):
            results.append(fail("core acceptance runtime entry must be an object"))
            continue
        symbol = str(entry.get("symbol", "")).strip()
        if not symbol:
            results.append(fail("core acceptance runtime entry missing symbol"))
            continue
        try:
            payload = _run_stock_diagnose(symbol, limit)
        except Exception as exc:
            results.append(fail(f"{symbol} runtime stock_diagnose failed: {exc}"))
            continue

        runtime_results = check_stock_diagnose_payload(payload, entry)
        failures = [
            str(item["message"]) for item in runtime_results if not bool(item["passed"])
        ]
        if failures:
            results.append(
                fail(f"{symbol} runtime acceptance failed: {'; '.join(failures)}")
            )
        else:
            results.append(ok(f"{symbol} runtime acceptance passed"))

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


def check_output_path_contract() -> list[dict[str, str | bool]]:
    cli = ROOT / "scripts" / "stock_replay_cli.py"
    renderer = ROOT / "scripts" / "render_replay_markdown.py"
    env_config = ROOT / "scripts" / "lib" / "env_config.py"
    cli_text = cli.read_text(encoding="utf-8") if cli.exists() else ""
    renderer_text = renderer.read_text(encoding="utf-8") if renderer.exists() else ""
    env_config_text = (
        env_config.read_text(encoding="utf-8") if env_config.exists() else ""
    )
    results: list[dict[str, str | bool]] = []

    if (
        'OUTPUT_DIR = _env_path("SRW_OUTPUT_DIR", PROJECT_ROOT / ".analysis")'
        not in env_config_text
    ):
        results.append(
            fail("env_config.py does not anchor OUTPUT_DIR default under .analysis")
        )
    else:
        results.append(ok("env_config.py anchors OUTPUT_DIR default under .analysis"))

    if "DEFAULT_OUTPUT_DIR = env_config.OUTPUT_DIR" not in cli_text:
        results.append(
            fail("stock_replay_cli.py does not take default output dir from env_config")
        )
    else:
        results.append(
            ok("stock_replay_cli.py takes default output dir from env_config")
        )

    if "output.parent.mkdir(parents=True, exist_ok=True)" not in renderer_text:
        results.append(
            fail("render_replay_markdown.py does not create missing parent directories")
        )
    else:
        results.append(
            ok("render_replay_markdown.py creates missing parent directories")
        )

    return results


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
        ([sys.executable, str(cli), "irm-qa", "--help"], "irm-qa --help works"),
        (
            [sys.executable, str(cli), "option-codes", "--help"],
            "option-codes --help works",
        ),
        (
            [sys.executable, str(cli), "option-tquote", "--help"],
            "option-tquote --help works",
        ),
        (
            [sys.executable, str(cli), "option-greeks", "--help"],
            "option-greeks --help works",
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
        check_core_acceptance_standards,
        check_core_acceptance_runtime,
        check_cli_structure,
        check_cli_help,
        check_script_help,
        check_output_path_contract,
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
