#!/usr/bin/env python3
"""Verify that a skill directory is a complete, packageable plugin.

Contract source: references/doctor.md — maintainer-checkout mode is keyed on
the presence of `scripts/verify-plugin-package.py`, and doctor.md check 4
defines the plugin wiring surface (commands/*.md and prompts/*.md routing to
their references). The md does not describe this script beyond its name and
that role, so it implements package integrity at the plain meaning:

1. SKILL.md exists, carries YAML frontmatter with `name` and `description`,
   and `name` matches the skill directory name.
2. references/, scripts/, and assets/ exist and are non-empty.
3. assets/template-motion.html exists — the canonical motion controller that
   self_check.py / lint-skin.py / verify-motion.py all resolve against.
4. Plugin wiring per doctor.md check 4: when a commands/ or prompts/ tree is
   present, every mapped file must exist and mention its target reference
   path. When neither tree exists the wiring check is not applicable (the
   installed-skill layout), which doctor.md explicitly says is not a failure.

Assumption: side-specific runtime scripts (e.g. excalidraw_extract.py) are
doctor's own check, not a package-integrity concern, so they are not
re-verified here.

Usage:
    python3 verify-plugin-package.py [SKILL_ROOT]

Exit codes: 0 package complete, 1 at least one finding.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SKILL_ROOT = SCRIPT_DIR.parent

# doctor.md check 4 routing map.
COMMAND_WIRING = {
    "export-diagram.md": "references/export.md",
    "import-drawio.md": "references/import-drawio.md",
    "import-mermaid.md": "references/import-mermaid.md",
    "profile.md": "references/profiles.md",
    "doctor.md": "references/doctor.md",
}
PROMPT_WIRING = {
    "export-diagram.md": "references/export.md",
    "import-mermaid.md": "references/import-mermaid.md",
    "profile.md": "references/profiles.md",
    "doctor.md": "references/doctor.md",
}
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*:")


def frontmatter(skill_md: Path) -> dict[str, str] | None:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            fields[match.group(1)] = line.split(":", 1)[1].strip()
    return None


def verify(skill_root: Path) -> list[str]:
    findings: list[str] = []
    if not skill_root.is_dir():
        return [f"{skill_root}: not a directory"]

    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        findings.append("SKILL.md is missing")
    else:
        fields = frontmatter(skill_md)
        if fields is None:
            findings.append("SKILL.md has no YAML frontmatter block")
        else:
            if not fields.get("name"):
                findings.append("SKILL.md frontmatter is missing `name`")
            elif fields["name"] != skill_root.name:
                findings.append(
                    f"SKILL.md name {fields['name']!r} does not match directory "
                    f"name {skill_root.name!r}"
                )
            if not fields.get("description"):
                findings.append("SKILL.md frontmatter is missing `description`")

    for directory in ("references", "scripts", "assets"):
        folder = skill_root / directory
        if not folder.is_dir():
            findings.append(f"{directory}/ directory is missing")
        elif not any(folder.iterdir()):
            findings.append(f"{directory}/ directory is empty")

    if not (skill_root / "assets" / "template-motion.html").is_file():
        findings.append(
            "assets/template-motion.html (canonical motion controller) is missing"
        )

    wiring_trees = [
        (folder, wiring)
        for folder, wiring in (
            (skill_root / "commands", COMMAND_WIRING),
            (skill_root / "prompts", PROMPT_WIRING),
        )
        if folder.is_dir()
    ]
    if not wiring_trees:
        print(
            "note: commands/ and prompts/ wiring not applicable (installed-skill layout)"
        )
    for folder, wiring in wiring_trees:
        for filename, reference in wiring.items():
            entry = folder / filename
            if not entry.is_file():
                findings.append(
                    f"{folder.name}/{filename} is missing (doctor.md check 4)"
                )
                continue
            if reference not in entry.read_text(encoding="utf-8"):
                findings.append(
                    f"{folder.name}/{filename} does not route to {reference}"
                )
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
        print(f"FAIL plugin-package {args.skill_root}")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"OK plugin-package {args.skill_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
