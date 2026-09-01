from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AssessmentError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def resolve_path(document: dict[str, Any], dotted_path: str) -> Any:
    current: Any = document
    for segment in dotted_path.split("."):
        if not isinstance(current, dict) or segment not in current:
            raise KeyError(dotted_path)
        current = current[segment]
    return current


def _validate_policy(policy: dict[str, Any]) -> None:
    controls = policy.get("controls")
    if not isinstance(controls, list) or not controls:
        raise AssessmentError("policy.controls must be a non-empty list")
    seen: set[str] = set()
    for control in controls:
        for key in ("id", "family", "title", "path", "expected"):
            if key not in control:
                raise AssessmentError(f"control missing required key: {key}")
        if control["id"] in seen:
            raise AssessmentError(f"duplicate control id: {control['id']}")
        seen.add(control["id"])


def assess(posture: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _validate_policy(policy)
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
            "rationale": control.get("rationale", ""),
        })

    return {
        "schema_version": "1.0",
        "assessed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall": "pass" if counts["gap"] == 0 else "with_gaps",
        "summary": {**counts, "applicable": counts["pass"] + counts["gap"], "total": len(results)},
        "input_sha256": digest(posture),
        "policy_sha256": digest(policy),
        "results": results,
        "non_claims": [
            "A passing local assessment does not prove deployed AWS configuration.",
            "A passing local assessment does not prove effective tenant isolation.",
            "This report does not establish certification, regulatory compliance or customer acceptance.",
        ],
    }


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssessmentError(f"{path} must contain a JSON object")
    return value
