#!/usr/bin/env python3
"""Verify the draw.io import extractor end to end.

Contract source: references/doctor.md check 3 lists
`scripts/verify-drawio-import.py` as a required maintainer-checkout script;
references/import-drawio.md owns the import flow itself. The md does not
describe the verifier beyond its name, so it implements the plain meaning:
prove that scripts/drawio_extract.py still round-trips representative draw.io
input through its documented interface.

Fixtures (generated in a temporary directory, nothing is written to the repo):
1. Raw-XML `mxfile` — two vertices and one labelled edge; must exit 0 and the
   `--json` IR must carry both node labels and the edge endpoints.
2. Compressed page payload — the same mxGraphModel URL-encoded, raw-deflated,
   and base64-wrapped the way draw.io writes `<diagram>` bodies; must decode
   to the same IR (exercises drawio_extract's inflate path).
3. Garbage input — must exit 2 (unreadable/unsupported), per drawio_extract's
   documented exit codes.

Assumption: the extractor is driven as a black box through
`sys.executable drawio_extract.py ...` so the gate covers the shipped CLI
contract (exit codes, --json shape), not internal functions.

Usage:
    python3 verify-drawio-import.py

Exit codes: 0 all fixtures behave as documented, 1 any finding.
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACTOR = SCRIPT_DIR / "drawio_extract.py"

MODEL_XML = (
    '<mxGraphModel dx="800" dy="600" grid="1" pageWidth="850" pageHeight="1100">'
    "<root>"
    '<mxCell id="0"/>'
    '<mxCell id="1" parent="0"/>'
    '<mxCell id="n1" value="Sensor" style="rounded=1;" vertex="1" parent="1">'
    '<mxGeometry x="40" y="40" width="120" height="60" as="geometry"/></mxCell>'
    '<mxCell id="n2" value="Gateway" style="rounded=1;" vertex="1" parent="1">'
    '<mxGeometry x="240" y="40" width="120" height="60" as="geometry"/></mxCell>'
    '<mxCell id="e1" value="MQTT" style="edgeStyle=orthogonalEdgeStyle;" edge="1" '
    'parent="1" source="n1" target="n2">'
    '<mxGeometry relative="1" as="geometry"/></mxCell>'
    "</root></mxGraphModel>"
)
RAW_MXFILE = (
    '<mxfile host="verify-drawio-import">'
    f'<diagram id="p1" name="Page-1">{MODEL_XML}</diagram>'
    "</mxfile>"
)


def compressed_mxfile() -> str:
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    payload = compressor.compress(quote(MODEL_XML).encode("utf-8"))
    payload += compressor.flush()
    encoded = base64.b64encode(payload).decode("ascii")
    return (
        '<mxfile host="verify-drawio-import">'
        f'<diagram id="p1" name="Page-1">{encoded}</diagram>'
        "</mxfile>"
    )


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


def check_ir(label: str, payload: dict, findings: list[str]) -> None:
    pages = payload.get("pages", [])
    if len(pages) != 1:
        findings.append(f"{label}: expected 1 page in the IR; got {len(pages)}")
        return
    page = pages[0]
    labels = {node.get("label") for node in page.get("nodes", [])}
    if not {"Sensor", "Gateway"} <= labels:
        findings.append(
            f"{label}: node labels Sensor/Gateway missing from {sorted(labels)}"
        )
    edges = page.get("edges", [])
    if len(edges) != 1:
        findings.append(f"{label}: expected 1 edge; got {len(edges)}")
        return
    edge = edges[0]
    if (edge.get("source"), edge.get("target")) != ("n1", "n2"):
        findings.append(
            f"{label}: edge endpoints are ({edge.get('source')}, {edge.get('target')}), "
            "expected (n1, n2)"
        )


def verify() -> list[str]:
    findings: list[str] = []
    if not EXTRACTOR.is_file():
        return [f"{EXTRACTOR} is missing"]
    with tempfile.TemporaryDirectory(prefix="verify-drawio-") as workdir:
        work = Path(workdir)

        raw = work / "raw.drawio"
        raw.write_text(RAW_MXFILE, encoding="utf-8")
        raw_out = work / "raw.json"
        result = run_extractor(raw, raw_out)
        if result.returncode != 0:
            findings.append(
                f"raw-xml fixture exited {result.returncode}: {result.stderr.strip()}"
            )
        else:
            check_ir(
                "raw-xml", json.loads(raw_out.read_text(encoding="utf-8")), findings
            )

        compressed = work / "compressed.drawio"
        compressed.write_text(compressed_mxfile(), encoding="utf-8")
        compressed_out = work / "compressed.json"
        result = run_extractor(compressed, compressed_out)
        if result.returncode != 0:
            findings.append(
                f"compressed-payload fixture exited {result.returncode}: {result.stderr.strip()}"
            )
        else:
            check_ir(
                "compressed-payload",
                json.loads(compressed_out.read_text(encoding="utf-8")),
                findings,
            )

        garbage = work / "garbage.drawio"
        garbage.write_text("this is not a draw.io file", encoding="utf-8")
        result = run_extractor(garbage, work / "garbage.json")
        if result.returncode != 2:
            findings.append(
                f"garbage fixture must exit 2 (unreadable/unsupported); got {result.returncode}"
            )
    return findings


def main() -> int:
    findings = verify()
    if findings:
        print("FAIL verify-drawio-import")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(
        "OK verify-drawio-import: raw-xml, compressed-payload, and garbage fixtures behave as documented"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
