from __future__ import annotations

import json
from pathlib import Path

from saassecops.cli import build_parser
from saassecops.stable_contract import contract_fingerprint, stable_contract_descriptor


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "contracts" / "v1-candidate.json"
FINGERPRINT = ROOT / "contracts" / "v1-candidate.sha256"


def main() -> int:
    expected = json.loads(BASELINE.read_text(encoding="utf-8"))
    actual = stable_contract_descriptor(build_parser())
    if actual != expected:
        raise SystemExit(
            "stable public contract changed; update the candidate baseline only with an explicit migration decision"
        )

    expected_fingerprint = FINGERPRINT.read_text(encoding="utf-8").strip()
    actual_fingerprint = contract_fingerprint(actual)
    if actual_fingerprint != expected_fingerprint:
        raise SystemExit("stable public contract fingerprint mismatch")

    print(f"stable contract candidate verified: sha256:{actual_fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
