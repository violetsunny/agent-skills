#!/usr/bin/env python3
"""Structural verifier for Traceable block decomposition registries.

Contract source — references/export-registry.md:
- "Validates ID uniqueness, parent resolution, or cycles. That's
  scripts/verify-block-registry.py — run it as its own step, not implied by
  export."
- "A duplicate ID is a correctness problem for scripts/verify-block-registry.py
  to catch"; "data-block-parent pointing at an ID absent from the file, or a
  parent cycle: ... scripts/verify-block-registry.py is the structural check".

Input is either an exported `.registry.json` sidecar or the source diagram
HTML; for HTML the blocks are read exactly the way export-registry.md defines
the projection (every element carrying data-block-id, document order,
data-block-* attributes verbatim).

Checks:
1. ID uniqueness — every duplicate occurrence is reported.
2. Parent resolution — every data-block-parent / "parent" value must name an
   ID present in the same file.
3. Parent cycles — including self-parenting; each node participating in a
   cycle is reported once.
4. Required keys — "id" and "name" are "always present; every block in the
   pattern requires both attributes" per the registry schema, so a missing
   name is a structural finding (the export projection itself never
   validates it).

Usage:
    python3 verify-block-registry.py FILE.registry.json | FILE.html

Exit codes: 0 structurally sound, 1 at least one finding.
"""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCK_ATTRIBUTES = (
    "id",
    "parent",
    "name",
    "input",
    "output",
    "constraint",
    "assumption",
    "impl",
)


class BlockParser(HTMLParser):
    """Collect data-block-* attribute sets in document order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.casefold(): value or "" for key, value in attrs}
        if "data-block-id" not in data:
            return
        block: dict[str, str] = {}
        for name in BLOCK_ATTRIBUTES:
            value = data.get(f"data-block-{name}")
            if value is not None:
                block[name] = value.strip()
        self.blocks.append(block)


def load_blocks(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            return [], [f"{path.name}: invalid JSON ({exc})"]
        if not isinstance(payload, dict) or not isinstance(payload.get("blocks"), list):
            return [], [f"{path.name}: registry must be an object with a blocks array"]
        blocks: list[dict[str, str]] = []
        findings: list[str] = []
        for index, entry in enumerate(payload["blocks"], 1):
            if not isinstance(entry, dict):
                findings.append(f"block {index}: entry is not an object")
                continue
            blocks.append(
                {
                    key: str(value)
                    for key, value in entry.items()
                    if isinstance(value, str)
                }
            )
        return blocks, findings
    parser = BlockParser()
    parser.feed(text)
    parser.close()
    if not parser.blocks:
        return [], [
            f"{path.name}: no data-block-id attributes found — not a Traceable block decomposition"
        ]
    return parser.blocks, []


def verify(path: Path) -> list[str]:
    blocks, findings = load_blocks(path)
    if findings and not blocks:
        return findings

    ids = [block.get("id", "") for block in blocks]
    for index, block in enumerate(blocks, 1):
        if not block.get("id"):
            findings.append(f"block {index}: missing required key id")
        if not block.get("name"):
            findings.append(
                f"block {index} ({block.get('id', '?')}): missing required key name"
            )

    seen: set[str] = set()
    for index, block_id in enumerate(ids, 1):
        if block_id and block_id in seen:
            findings.append(f"duplicate block id {block_id!r} at entry {index}")
        seen.add(block_id)

    parents = {
        block.get("id", ""): block.get("parent", "")
        for block in blocks
        if block.get("id")
    }
    for block_id, parent in parents.items():
        if parent and parent not in seen:
            findings.append(
                f"block {block_id!r}: parent {parent!r} is absent from the file"
            )

    # ponytail: O(n^2) walk of parent chains; registries are hand-authored and
    # small. Upgrade to color-marked DFS if registries ever exceed ~1k blocks.
    reported: set[frozenset[str]] = set()
    for start in parents:
        visited: set[str] = set()
        current = start
        while current and current in parents and current not in visited:
            visited.add(current)
            current = parents[current]
        if current and current in visited:
            cycle = [current]
            walker = parents[current]
            while walker != current:
                cycle.append(walker)
                walker = parents[walker]
            key = frozenset(cycle)
            if key not in reported:
                reported.add(key)
                findings.append(
                    "parent cycle among blocks: "
                    + ", ".join(repr(item) for item in sorted(cycle))
                )
    return findings


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argument_parser.add_argument(
        "file", type=Path, help=".registry.json or source .html"
    )
    args = argument_parser.parse_args()
    try:
        findings = verify(args.file)
    except (OSError, UnicodeError) as exc:
        findings = [str(exc)]
    if findings:
        print(f"FAIL {args.file}")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"OK {args.file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
