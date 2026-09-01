from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .contracts import ContractError, validate_document


class AssessmentError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: str | Path) -> str:
    return digest_bytes(Path(path).read_bytes())


def resolve_path(document: dict[str, Any], dotted_path: str) -> Any:
    current: Any = document
    for segment in dotted_path.split("."):
        if not isinstance(current, dict) or segment not in current:
            raise KeyError(dotted_path)
        current = current[segment]
    return current


def _validate_inputs(posture: dict[str, Any], policy: dict[str, Any]) -> None:
    try:
        validate_document(posture, "posture")
        validate_document(policy, "policy")
    except ContractError as exc:
        raise AssessmentError(str(exc)) from exc

    ids = [control["id"] for control in policy["controls"]]
    if len(ids) != len(set(ids)):
        raise AssessmentError("policy control ids must be unique")


def assess(posture: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _validate_inputs(posture, policy)
    results: list[dict[str, Any]] = []
    counts = {"pass": 0, "gap": 0, "not_applicable": 0}

    for control in sorted(policy["controls"], key=lambda item: item["id"]):
        try:
            actual = resolve_path(posture, control["path"])
            status = "pass" if actual == control["expected"] else "gap"
        except KeyError:
            actual = None
            status = "gap"

        counts[status] += 1
        results.append({
            "id": control["id"],
            "family": control["family"],
            "title": control["title"],
            "status": status,
            "path": control["path"],
            "expected": control["expected"],
            "actual": actual,
            "rationale": control["rationale"],
        })

    input_sha256 = digest(posture)
    policy_sha256 = digest(policy)
    assessment_id = digest({
        "schema_version": "1.0",
        "posture_id": posture["architecture_id"],
        "policy_id": policy["policy_id"],
        "input_sha256": input_sha256,
        "policy_sha256": policy_sha256,
    })

    report = {
        "schema_version": "1.0",
        "tool": {"name": "SaaSSecOps", "version": __version__},
        "posture_id": posture["architecture_id"],
        "policy_id": policy["policy_id"],
        "assessed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "assessment_id": assessment_id,
        "overall": "pass" if counts["gap"] == 0 else "with_gaps",
        "summary": {**counts, "applicable": counts["pass"] + counts["gap"], "total": len(results)},
        "input_sha256": input_sha256,
        "policy_sha256": policy_sha256,
        "results": results,
        "non_claims": [
            "A passing local assessment does not prove deployed AWS configuration.",
            "A passing local assessment does not prove effective tenant isolation.",
            "This report does not establish certification, regulatory compliance or customer acceptance.",
        ],
    }
    try:
        validate_document(report, "report")
    except ContractError as exc:
        raise AssessmentError(f"internal report contract failure: {exc}") from exc
    return report


def build_evidence_manifest(
    report: dict[str, Any],
    *,
    posture_name: str,
    policy_name: str,
    report_name: str,
    report_bytes: bytes,
) -> dict[str, Any]:
    manifest = {
        "schema_version": "1.0",
        "tool": {"name": "SaaSSecOps", "version": __version__},
        "assessment_id": report["assessment_id"],
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "subjects": {
            "posture": {"name": posture_name, "sha256": report["input_sha256"]},
            "policy": {"name": policy_name, "sha256": report["policy_sha256"]},
            "report": {"name": report_name, "sha256": digest_bytes(report_bytes)},
        },
    }
    try:
        validate_document(manifest, "manifest")
    except ContractError as exc:
        raise AssessmentError(f"internal manifest contract failure: {exc}") from exc
    return manifest


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssessmentError(f"{path} must contain a JSON object")
    return value
