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

class StableReleaseError(ValueError):
    pass

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def package_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["version"]

def verify_repository(source_sha: str) -> dict:
    if not SHA_RE.fullmatch(source_sha.lower()):
        raise StableReleaseError("source SHA must be 40 hexadecimal characters")
    stable = _load_json(ROOT / "release" / "v1-stable-checklist.json")
    rc = _load_json(ROOT / "release" / "v1-rc-checklist.json")
    defects = _load_json(ROOT / "release" / "defect-register.json")
    version = package_version()
    if version != stable["release_version"]:
        raise StableReleaseError("package version does not match stable release checklist")
    if stable["promoted_from"] != rc["candidate_version"]:
        raise StableReleaseError("stable release does not identify the checked release candidate")
    expected = stable["stable_contract_sha256"]
    rc_hash = rc["stable_contract_sha256"]
    checked = (ROOT / "contracts" / "v1-candidate.sha256").read_text(encoding="utf-8").strip()
    actual = contract_fingerprint(stable_contract_descriptor(build_parser()))
    if len({expected, rc_hash, checked, actual}) != 1:
        raise StableReleaseError("stable contract fingerprint changed during RC-to-v1 promotion")
    missing = [p for p in stable["required_documents"] if not (ROOT / p).is_file()]
    if missing:
        raise StableReleaseError("required stable release documents missing: " + ", ".join(missing))
    threat_text = (ROOT / "docs" / "THREAT_MODEL.md").read_text(encoding="utf-8")
    domains = ["Cloud and organization","Tenant isolation","Application and API security","Software supply chain","Customer trust","Evidence integrity","Incident response and operations"]
    missing_domains = [d for d in domains if d not in threat_text]
    if missing_domains:
        raise StableReleaseError("threat-model domains missing: " + ", ".join(missing_domains))
    blocking_severities = set(defects["review_policy"]["blocking_severities"])
    blocking_statuses = set(defects["review_policy"]["blocking_statuses"])
    blockers = [e for e in defects["entries"] if e.get("severity") in blocking_severities and e.get("status") in blocking_statuses]
    if blockers:
        raise StableReleaseError("blocking repository defects remain: " + ", ".join(e.get("id", "unidentified") for e in blockers))
    return {"schema_version":"1.0","release_version":version,"promoted_from":stable["promoted_from"],"source_sha":source_sha.lower(),"stable_contract_sha256":actual,"rc_contract_continuity":"pass","required_repository_gate_count":len(stable["required_repository_gates"]),"required_document_count":len(stable["required_documents"]),"threat_model_domains_reviewed":domains,"open_repository_high_critical_defects":0,"repository_review":"pass","external_required_gates":stable["required_external_gates"],"non_claims":stable["non_claims"]}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        report = verify_repository(args.source_sha)
    except (OSError, KeyError, json.JSONDecodeError, StableReleaseError) as exc:
        parser.error(str(exc))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
