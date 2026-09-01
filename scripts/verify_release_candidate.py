from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path

from saassecops.cli import build_parser
from saassecops.stable_contract import contract_fingerprint, stable_contract_descriptor


ROOT = Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ReleaseCandidateError(ValueError):
    pass


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def package_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["version"]


def verify_repository(source_sha: str) -> dict:
    if not SHA_RE.fullmatch(source_sha.lower()):
        raise ReleaseCandidateError("source SHA must be 40 hexadecimal characters")

    checklist = _load_json(ROOT / "release" / "v1-rc-checklist.json")
    defects = _load_json(ROOT / "release" / "defect-register.json")

    version = package_version()
    if version != checklist["candidate_version"]:
        raise ReleaseCandidateError("package version does not match release-candidate checklist")

    expected_fingerprint = checklist["stable_contract_sha256"]
    checked_fingerprint = (ROOT / "contracts" / "v1-candidate.sha256").read_text(encoding="utf-8").strip()
    actual_fingerprint = contract_fingerprint(stable_contract_descriptor(build_parser()))
    if expected_fingerprint != checked_fingerprint or checked_fingerprint != actual_fingerprint:
        raise ReleaseCandidateError("stable contract fingerprint mismatch")

    missing_docs = [path for path in checklist["required_documents"] if not (ROOT / path).is_file()]
    if missing_docs:
        raise ReleaseCandidateError(f"required release documents missing: {', '.join(missing_docs)}")

    threat_text = (ROOT / "docs" / "THREAT_MODEL.md").read_text(encoding="utf-8")
    required_domains = [
        "Cloud and organization",
        "Tenant isolation",
        "Application and API security",
        "Software supply chain",
        "Customer trust",
        "Evidence integrity",
        "Incident response and operations",
    ]
    missing_domains = [domain for domain in required_domains if domain not in threat_text]
    if missing_domains:
        raise ReleaseCandidateError(f"threat-model domains missing: {', '.join(missing_domains)}")

    blocking_severities = set(defects["review_policy"]["blocking_severities"])
    blocking_statuses = set(defects["review_policy"]["blocking_statuses"])
    blockers = [
        entry for entry in defects["entries"]
        if entry.get("severity") in blocking_severities and entry.get("status") in blocking_statuses
    ]
    if blockers:
        ids = ", ".join(entry.get("id", "unidentified") for entry in blockers)
        raise ReleaseCandidateError(f"blocking repository defects remain: {ids}")

    return {
        "schema_version": "1.0",
        "candidate_version": version,
        "source_sha": source_sha.lower(),
        "stable_contract_sha256": actual_fingerprint,
        "required_repository_gate_count": len(checklist["required_repository_gates"]),
        "required_document_count": len(checklist["required_documents"]),
        "threat_model_domains_reviewed": required_domains,
        "open_repository_high_critical_defects": 0,
        "repository_review": "pass",
        "external_required_gates": checklist["required_external_gates"],
        "non_claims": checklist["non_claims"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        report = verify_repository(args.source_sha)
    except (OSError, KeyError, json.JSONDecodeError, ReleaseCandidateError) as exc:
        parser.error(str(exc))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
