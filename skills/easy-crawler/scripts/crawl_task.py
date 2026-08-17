#!/usr/bin/env python3

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from importlib.util import find_spec
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


SOCIAL_PAGE_TYPES = {"search", "timeline", "creator", "comments"}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def slugify(text):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return value or "target"


def extract_title(body):
    match = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return title or None


def build_discovery_target(source_target, strategy, index):
    source_value = (
        source_target.get("url") or source_target.get("page_type") or "target"
    )
    source_url = source_target.get("url")
    if not source_url:
        return f"{source_value}:discovered:{index}"

    parsed = urlparse(source_url)
    base = (
        f"{parsed.scheme}://{parsed.netloc}"
        if parsed.scheme and parsed.netloc
        else source_url
    )
    normalized_path = parsed.path.rstrip("/")

    if strategy == "follow_links":
        if normalized_path:
            return f"{base}{normalized_path}/discovered-{index}"
        return f"{base}/discovered-{index}"
    if strategy == "search_results":
        return f"{base}/post/discovered-{index}"
    if strategy == "timeline_window":
        return f"{base}/timeline/discovered-{index}"
    return f"{source_url}#discovered-{index}"


def build_discovered_targets(task, runtime_errors, execute):
    discovery = task.get("discovery") or {}
    strategy = discovery.get("strategy") or "none"
    if execute or strategy == "none":
        return []

    blocking_codes = {"validation_error", "requires_dedicated_adaptation"}
    if any(error.get("code") in blocking_codes for error in runtime_errors):
        return []

    max_discovered_targets = discovery.get("max_discovered_targets") or 0
    preview_limit = min(max_discovered_targets if max_discovered_targets > 0 else 1, 3)
    checkpoint_key = discovery.get("checkpoint_key")
    discovered_targets = []

    for target in task.get("targets", []):
        source_target = target.get("url") or target.get("page_type") or "target"
        for index in range(1, preview_limit + 1):
            record_id = None if strategy == "follow_links" else f"preview-{index}"
            checkpoint = None
            if checkpoint_key:
                checkpoint = {
                    "checkpoint_key": checkpoint_key,
                    "checkpoint_value": f"preview-{index}",
                }

            discovered_targets.append(
                {
                    "source_target": source_target,
                    "discovery_type": strategy,
                    "target": build_discovery_target(target, strategy, index),
                    "record_id": record_id,
                    "status": "discovered",
                    "checkpoint": checkpoint,
                    "placeholder": True,
                }
            )

    return discovered_targets


def validate_task(task):
    errors = []
    for key in ("task_name", "targets", "extraction", "run"):
        if key not in task:
            errors.append(
                {
                    "code": "validation_error",
                    "message": f"Missing required top-level field: {key}",
                    "hint": "Read references/task-syntax.md and restore the required field.",
                }
            )

    targets = task.get("targets")
    if not isinstance(targets, list) or not targets:
        errors.append(
            {
                "code": "validation_error",
                "message": "Field 'targets' must be a non-empty array.",
                "hint": "Provide at least one crawl target.",
            }
        )
        return errors

    for index, target in enumerate(targets, start=1):
        if not isinstance(target, dict):
            errors.append(
                {
                    "code": "validation_error",
                    "message": f"Target #{index} must be an object.",
                    "hint": "Use the target schema from references/task-syntax.md.",
                }
            )
            continue

        if not target.get("url") and not target.get("page_type"):
            errors.append(
                {
                    "code": "validation_error",
                    "message": f"Target #{index} must include at least 'url' or 'page_type'.",
                    "hint": "Declare the crawl target explicitly.",
                }
            )

        if not target.get("page_type"):
            errors.append(
                {
                    "code": "validation_error",
                    "message": f"Target #{index} is missing 'page_type'.",
                    "hint": "Declare one of: list, detail, search, timeline, creator, comments.",
                }
            )

    social = task.get("social") or {}
    browser = (task.get("run") or {}).get("browser") or {}
    if social.get("login_state") == "required" and not browser.get(
        "storage_state_path"
    ):
        errors.append(
            {
                "code": "validation_error",
                "message": "login_state is required but browser.storage_state_path is missing.",
                "hint": "Provide a reusable storage state file or relax login_state.",
            }
        )

    if social.get("include_replies") and not social.get("include_comments"):
        errors.append(
            {
                "code": "validation_error",
                "message": "include_replies=true requires include_comments=true.",
                "hint": "Enable comment capture before requesting nested replies.",
            }
        )

    discovery = task.get("discovery") or {}
    if discovery.get("resume_from_checkpoint") and not discovery.get("checkpoint_key"):
        errors.append(
            {
                "code": "checkpoint_state_missing",
                "message": "resume_from_checkpoint is true but discovery.checkpoint_key is missing.",
                "hint": "Declare which checkpoint key the caller will use to resume discovery.",
            }
        )

    return errors


def select_mode(task, override_mode=None):
    if override_mode:
        return override_mode, ["cli_override"]

    run = task.get("run") or {}
    requested_mode = run.get("mode", "auto")
    if requested_mode == "http":
        return "http", ["requested_http_mode"]
    if requested_mode == "browser":
        return "browser", ["requested_browser_mode"]

    reasons = []
    browser = run.get("browser") or {}
    social = task.get("social") or {}
    anti_bot = task.get("anti_bot") or {}
    for target in task.get("targets", []):
        if target.get("requires_js"):
            reasons.append("target_requires_js")
        if target.get("page_type") in SOCIAL_PAGE_TYPES:
            reasons.append(f"social_page_type:{target.get('page_type')}")

    if browser.get("required"):
        reasons.append("browser_required")
    if social.get("dynamic_rendering"):
        reasons.append("social_dynamic_rendering")
    if social.get("login_state") == "required":
        reasons.append("social_login_required")
    if social.get("include_comments"):
        reasons.append("social_comments_requested")
    if social.get("include_replies"):
        reasons.append("social_replies_requested")
    if anti_bot.get("real_browser"):
        reasons.append("real_browser_requested")

    if reasons:
        return "browser", reasons
    return "http", ["auto_default_http"]


def capability_issues(task, selected_mode):
    issues = []
    platform = task.get("platform") or {}
    anti_bot = task.get("anti_bot") or {}

    if platform.get("requires_signing"):
        issues.append(
            {
                "code": "requires_dedicated_adaptation",
                "message": "Task requires proprietary signing not supported by v0.2.",
                "hint": "Use a dedicated platform adapter instead of the generic crawler contract.",
            }
        )

    if anti_bot.get("requires_captcha_solver"):
        issues.append(
            {
                "code": "requires_dedicated_adaptation",
                "message": "CAPTCHA solving is outside the supported boundary for v0.2.",
                "hint": "Switch to manual intervention or a dedicated authorized workflow.",
            }
        )

    if selected_mode == "browser" and find_spec("playwright") is None:
        issues.append(
            {
                "code": "missing_browser_dependency",
                "message": "Browser mode was selected but Playwright is not installed in the current Python environment.",
                "hint": "Install requirements-browser.txt before attempting browser execution.",
            }
        )

    return issues


def make_record(target, status, title=None, content_type=None, extra=None):
    payload = {
        "target": target.get("url") or target.get("page_type"),
        "page_type": target.get("page_type"),
        "status": status,
        "title": title,
        "content_type": content_type,
    }
    if extra:
        payload.update(extra)
    return payload


def fetch_http_target(target, output_dir, task):
    http_cfg = (task.get("run") or {}).get("http") or {}
    artifacts_cfg = task.get("artifacts") or {}
    timeout_seconds = http_cfg.get("timeout_seconds", 20)
    user_agent = http_cfg.get("user_agent", "easy-crawler/0.2")
    url = target.get("url")
    request = Request(url, headers={"User-Agent": user_agent})
    debug_items = []

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            body_bytes = response.read()
            content_type = response.headers.get_content_type()
            final_url = response.geturl()
            body_text = body_bytes.decode("utf-8", errors="replace")
            title = extract_title(body_text)

            if artifacts_cfg.get("capture_html", True) and content_type == "text/html":
                parsed = urlparse(final_url)
                html_dir = output_dir / "debug" / "html"
                html_dir.mkdir(parents=True, exist_ok=True)
                html_path = html_dir / f"{slugify(parsed.netloc + parsed.path)}.html"
                html_path.write_text(body_text, encoding="utf-8")
                debug_items.append(
                    {
                        "type": "html_dump",
                        "path": str(html_path),
                        "target": final_url,
                    }
                )

            return (
                make_record(
                    target,
                    "ok",
                    title=title,
                    content_type=content_type,
                    extra={"final_url": final_url},
                ),
                [],
                debug_items,
            )
    except HTTPError as exc:
        return (
            make_record(target, "failed"),
            [
                {
                    "code": "http_fetch_failed",
                    "message": f"HTTP error {exc.code} while fetching {url}.",
                    "hint": "Check the target URL, rate limits, or switch to browser mode if the page requires JS/auth.",
                }
            ],
            debug_items,
        )
    except URLError as exc:
        return (
            make_record(target, "failed"),
            [
                {
                    "code": "http_fetch_failed",
                    "message": f"URL error while fetching {url}: {exc.reason}",
                    "hint": "Verify network access, DNS, proxy settings, or target availability.",
                }
            ],
            debug_items,
        )


def build_outputs(
    task,
    selected_mode,
    selection_reasons,
    execute,
    validation_errors,
    capability_errors,
    output_dir,
):
    records = []
    runtime_errors = list(validation_errors) + list(capability_errors)
    debug_artifacts = []
    discovered_targets = build_discovered_targets(task, runtime_errors, execute)

    if validation_errors:
        for target in task.get("targets", []):
            records.append(make_record(target, "failed"))
    elif selected_mode == "browser" and execute:
        for target in task.get("targets", []):
            records.append(make_record(target, "unsupported"))
        runtime_errors.append(
            {
                "code": "browser_backend_not_implemented",
                "message": "Browser mode contract is defined, but the v0.2 browser execution backend is not implemented yet.",
                "hint": "Use dry-run for planning or add a dedicated browser backend in a follow-up change.",
            }
        )
    elif execute and selected_mode == "http" and not capability_errors:
        for target in task.get("targets", []):
            record, errors, debug_items = fetch_http_target(target, output_dir, task)
            records.append(record)
            runtime_errors.extend(errors)
            debug_artifacts.extend(debug_items)
    else:
        for target in task.get("targets", []):
            status = "unsupported" if capability_errors else "planned"
            records.append(make_record(target, status))

    success_count = sum(1 for item in records if item["status"] == "ok")
    failure_count = sum(
        1 for item in records if item["status"] in {"failed", "unsupported"}
    )
    planned_count = sum(1 for item in records if item["status"] == "planned")

    result = {
        "task_name": task.get("task_name"),
        "selected_mode": selected_mode,
        "dry_run": not execute,
        "discovered_targets": discovered_targets,
        "records": records,
    }
    run_summary = {
        "task_name": task.get("task_name"),
        "selected_mode": selected_mode,
        "selection_reasons": selection_reasons,
        "target_count": len(task.get("targets", [])),
        "discovered_target_count": len(discovered_targets),
        "success_count": success_count,
        "failure_count": failure_count,
        "planned_count": planned_count,
        "discovery_strategy": (task.get("discovery") or {}).get("strategy", "none"),
        "checkpoint_key": (task.get("discovery") or {}).get("checkpoint_key"),
        "output_dir": str(output_dir),
        "started_at": now_iso(),
    }
    error_summary = {"errors": runtime_errors}
    debug_payload = {"artifacts": debug_artifacts}
    return result, run_summary, error_summary, debug_payload


def parse_args():
    parser = argparse.ArgumentParser(description="Standalone crawler task runner")
    parser.add_argument("--task", required=True, help="Path to task JSON file")
    parser.add_argument(
        "--output-dir", required=True, help="Directory for output artifacts"
    )
    parser.add_argument(
        "--mode", choices=["http", "browser"], help="Override task run mode"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the minimal backend instead of dry-run planning",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    task = read_json(args.task)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    validation_errors = validate_task(task)
    selected_mode, selection_reasons = select_mode(task, args.mode)
    capability_errors = capability_issues(task, selected_mode)
    result, run_summary, error_summary, debug_payload = build_outputs(
        task=task,
        selected_mode=selected_mode,
        selection_reasons=selection_reasons,
        execute=args.execute,
        validation_errors=validation_errors,
        capability_errors=capability_errors,
        output_dir=output_dir,
    )

    write_json(output_dir / "result.json", result)
    write_json(output_dir / "run-summary.json", run_summary)
    write_json(output_dir / "error-summary.json", error_summary)
    write_json(output_dir / "debug-artifacts.json", debug_payload)

    print(
        json.dumps(
            {
                "task_name": task.get("task_name"),
                "selected_mode": selected_mode,
                "output_dir": str(output_dir),
                "errors": len(error_summary["errors"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    if error_summary["errors"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
