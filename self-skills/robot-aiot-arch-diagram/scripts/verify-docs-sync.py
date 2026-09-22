#!/usr/bin/env python3
"""Verify documentation/file synchronization inside a skill package.

Contract source: references/doctor.md check 3 lists `scripts/verify-docs-sync.py`
as a required maintainer-checkout script; the md gives no further description,
so this implements the plain meaning of the name — docs and shipped files must
stay in sync: every local file path a doc points at must exist.

Checked references:
1. Markdown links `[text](target)` in SKILL.md, references/*.md, and
   commands/*.md + prompts/*.md when present. Targets with a URL scheme,
   pure anchors, angle-bracket placeholders, and `path/to/...` examples are
   skipped; anchors are stripped; relative targets resolve against the
   directory of the linking file.
2. Backticked repository paths that start with `scripts/` or `templates/`
   (optionally behind a `<repo-root>`/`<skill-dir>`-style placeholder prefix),
   resolved against the skill root. Prose examples under `assets/` or
   `references/` are deliberately not swept up: markdown-link checking already
   covers real doc references, while backticked asset paths are frequently
    hypothetical examples（如 export-registry.md 中的多图 gallery HTML 源示例，
    属用户源文件，不随 skill 分发）.

Assumption: "sync" is link integrity only. Reverse coverage (every file
mentioned from every doc) is not part of the contract and is not checked.

Usage:
    python3 verify-docs-sync.py [SKILL_ROOT]

Exit codes: 0 in sync, 1 at least one dangling reference.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SKILL_ROOT = SCRIPT_DIR.parent

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BACKTICK_PATH_RE = re.compile(
    r"`[^`]*?(?:<[^>]+>/)*((?:scripts|templates)/[A-Za-z0-9._/-]+\.[A-Za-z0-9]+)[^`]*?`"
)
SKIP_PREFIXES = ("path/to/", "example", "my-diagram", "…")
URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def markdown_files(skill_root: Path) -> list[Path]:
    candidates = [skill_root / "SKILL.md"]
    for directory in ("references", "commands", "prompts"):
        folder = skill_root / directory
        if folder.is_dir():
            candidates.extend(sorted(folder.glob("*.md")))
    return [path for path in candidates if path.is_file()]


def check_markdown_link(target: str, owner: Path, skill_root: Path) -> str | None:
    if target.startswith(("#", "<")) or URL_SCHEME_RE.match(target):
        return None
    if any(target.startswith(prefix) for prefix in SKIP_PREFIXES):
        return None
    resolved = (owner.parent / target.split("#", 1)[0]).resolve()
    if not resolved.exists():
        return f"markdown link target missing: {target}"
    return None


def check_backtick_path(target: str, skill_root: Path) -> str | None:
    if any(target.startswith(prefix) for prefix in SKIP_PREFIXES):
        return None
    if not (skill_root / target).is_file():
        return f"referenced repository file missing: {target}"
    return None


def verify(skill_root: Path) -> list[str]:
    if not skill_root.is_dir():
        return [f"{skill_root}: not a directory"]
    findings: list[str] = []
    for path in markdown_files(skill_root):
        relative = path.relative_to(skill_root)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in MARKDOWN_LINK_RE.finditer(line):
                finding = check_markdown_link(match.group(1), path, skill_root)
                if finding:
                    findings.append(f"{relative}:{number}: {finding}")
            for match in BACKTICK_PATH_RE.finditer(line):
                finding = check_backtick_path(match.group(1), skill_root)
                if finding:
                    findings.append(f"{relative}:{number}: {finding}")
    return findings


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argument_parser.add_argument(
        "skill_root",
        nargs="?",
        type=Path,
        default=DEFAULT_SKILL_ROOT,
        help="skill installation root (default: this script's skill)",
    )
    args = argument_parser.parse_args()
    findings = verify(args.skill_root)
    if findings:
        print(f"FAIL docs-sync {args.skill_root}")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"OK docs-sync {args.skill_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
