from __future__ import annotations

import argparse
import json
from pathlib import Path

from saassecops.contracts import validate_document
from saassecops.trust import summarize_customer_trust


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", default="architecture/customer-trust-reference.json")
    parser.add_argument("--questionnaire", default="examples/security-questionnaire.json")
    parser.add_argument("--exceptions", default="examples/trust-exceptions.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    reference = _load(args.reference)
    questionnaire = _load(args.questionnaire)
    exceptions = _load(args.exceptions)

    validate_document(reference, "customer-trust")
    validate_document(questionnaire, "questionnaire")
    validate_document(exceptions, "trust-exceptions")

    result = summarize_customer_trust(questionnaire, exceptions)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if result["ready_for_customer_use"]:
        raise SystemExit("synthetic questionnaire unexpectedly became customer-ready")

    expected_blocked = {"Q-002", "Q-003"}
    blockers = " ".join(result["questionnaire"]["blockers"])
    if not all(item in blockers for item in expected_blocked):
        raise SystemExit("expected unresolved questionnaire blockers were not preserved")

    return 0


def _load(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
