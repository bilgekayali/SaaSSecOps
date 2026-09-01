from __future__ import annotations

import json
from pathlib import Path

from saassecops.contracts import validate_document
from saassecops.isolation import run_vectors

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "architecture" / "tenant-isolation-reference.json"


def main() -> int:
    document = json.loads(REFERENCE.read_text(encoding="utf-8"))
    validate_document(document, "tenant-isolation")
    outcomes = run_vectors(document)

    mismatches = [
        outcome
        for outcome in outcomes
        if outcome["actual"] != outcome["expected"]
    ]

    print(json.dumps({"outcomes": outcomes}, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
