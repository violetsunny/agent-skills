#!/usr/bin/env python3
"""Verify the Mermaid import extractor end to end.

Contract source: references/doctor.md check 3 lists
`scripts/verify-mermaid-import.py` as a required maintainer-checkout script;
references/import-mermaid.md owns the import flow itself. The md does not
describe the verifier beyond its name, so it implements the plain meaning:
prove that scripts/mermaid_extract.py still parses representative Mermaid
input through its documented interface.

Fixtures (generated in a temporary directory, nothing is written to the repo):
1. A `flowchart TD` source with three shaped nodes and one labelled edge —
   must exit 0 and the `--json` IR must carry kind, direction, node ids, and
   the edge with its label.
2. An unsupported `pie` diagram — must exit 2, per mermaid_extract's
   documented exit codes ("unsupported" is a failure).

Assumption: the extractor is driven as a black box through
`sys.executable mermaid_extract.py ...` so the gate covers the shipped CLI
contract (exit codes, --json shape), not internal functions. Fixture labels
avoid quoted-edge-label syntax, whose handling differs between repository
sides' mermaid_extract.py revisions.

Usage:
    python3 verify-mermaid-import.py

Exit codes: 0 all fixtures behave as documented, 1 any finding.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACTOR = SCRIPT_DIR / "mermaid_extract.py"

FLOWCHART = "flowchart TD\n  a[Sensor] --> b{Gateway}\n  b -->|MQTT| c[Cloud]\n"
UNSUPPORTED = 'pie title Pets\n  "Dogs" : 386\n'


def run_extractor(fixture: Path, json_out: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(EXTRACTOR),
            str(fixture),
            "--json",
            "--out",
            str(json_out),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )


def verify() -> list[str]:
    findings: list[str] = []
    if not EXTRACTOR.is_file():
        return [f"{EXTRACTOR} is missing"]
    with tempfile.TemporaryDirectory(prefix="verify-mermaid-") as workdir:
        work = Path(workdir)

        source = work / "flow.mmd"
        source.write_text(FLOWCHART, encoding="utf-8")
        output = work / "flow.json"
        result = run_extractor(source, output)
        if result.returncode != 0:
            findings.append(
                f"flowchart fixture exited {result.returncode}: {result.stderr.strip()}"
            )
        else:
            payload = json.loads(output.read_text(encoding="utf-8"))
            diagrams = payload.get("diagrams", [])
            if len(diagrams) != 1:
                findings.append(f"expected 1 diagram in the IR; got {len(diagrams)}")
            else:
                diagram = diagrams[0]
                if diagram.get("kind") != "flowchart":
                    findings.append(
                        f"diagram kind is {diagram.get('kind')!r}, expected 'flowchart'"
                    )
                if diagram.get("direction") != "TD":
                    findings.append(
                        f"direction is {diagram.get('direction')!r}, expected 'TD'"
                    )
                node_ids = {node.get("id") for node in diagram.get("nodes", [])}
                if not {"a", "b", "c"} <= node_ids:
                    findings.append(f"node ids a/b/c missing from {sorted(node_ids)}")
                edges = diagram.get("edges", [])
                if len(edges) != 2:
                    findings.append(f"expected 2 edges; got {len(edges)}")
                else:
                    labelled = [edge for edge in edges if edge.get("label") == "MQTT"]
                    if len(labelled) != 1 or (
                        labelled[0].get("source"),
                        labelled[0].get("target"),
                    ) != ("b", "c"):
                        findings.append(
                            f"expected exactly one MQTT edge b->c; got {edges}"
                        )

        unsupported = work / "pie.mmd"
        unsupported.write_text(UNSUPPORTED, encoding="utf-8")
        result = run_extractor(unsupported, work / "pie.json")
        if result.returncode != 2:
            findings.append(
                f"unsupported-kind fixture must exit 2; got {result.returncode}"
            )
    return findings


def main() -> int:
    findings = verify()
    if findings:
        print("FAIL verify-mermaid-import")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(
        "OK verify-mermaid-import: flowchart and unsupported-kind fixtures behave as documented"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
