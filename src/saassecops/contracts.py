from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


class ContractError(ValueError):
    pass


SCHEMA_FILES = {
    "posture": "security-posture.schema.json",
    "policy": "control-policy.schema.json",
    "report": "assessment-report.schema.json",
    "manifest": "evidence-manifest.schema.json",
    "multi-account": "multi-account-reference.schema.json",
    "tenant-isolation": "tenant-isolation-reference.schema.json",
    "appsec": "appsec-reference.schema.json",
    "vulnerability-evidence": "vulnerability-evidence.schema.json",
    "customer-trust": "customer-trust-reference.schema.json",
    "questionnaire": "security-questionnaire-response.schema.json",
    "trust-exceptions": "trust-exception-register.schema.json",
}


def schema_document(kind: str) -> dict[str, Any]:
    try:
        filename = SCHEMA_FILES[kind]
    except KeyError as exc:
        raise ContractError(f"unsupported contract kind: {kind}") from exc
    text = files("saassecops").joinpath("schemas", filename).read_text(encoding="utf-8")
    return json.loads(text)


def validate_document(document: dict[str, Any], kind: str) -> None:
    schema = schema_document(kind)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    if not errors:
        return
    first = errors[0]
    path = ".".join(str(part) for part in first.absolute_path) or "$"
    raise ContractError(f"{kind} contract violation at {path}: {first.message}")


def contract_snapshot(version: str) -> dict[str, Any]:
    return {
        "tool": {"name": "SaaSSecOps", "version": version},
        "commands": ["assess", "contract-snapshot", "digest", "validate"],
        "schemas": {
            kind: schema_document(kind)["$id"]
            for kind in sorted(SCHEMA_FILES)
        },
        "assessment_schema_version": "1.0",
        "evidence_manifest_schema_version": "1.0",
        "multi_account_schema_version": "1.0",
        "tenant_isolation_schema_version": "1.0",
        "appsec_schema_version": "1.0",
        "vulnerability_evidence_schema_version": "1.0",
        "customer_trust_schema_version": "1.0",
        "questionnaire_schema_version": "1.0",
        "trust_exception_schema_version": "1.0",
    }
