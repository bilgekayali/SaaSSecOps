from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class TrustCheck:
    ready: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]


def evaluate_questionnaire(document: dict[str, Any]) -> TrustCheck:
    blockers: list[str] = []
    warnings: list[str] = []

    for response in document.get("responses", []):
        response_id = response.get("id", "<unknown>")
        answer = response.get("answer")
        evidence = response.get("evidence", [])
        claim_strength = response.get("claim_strength")
        review = response.get("review", {})
        customer_safe_answer = response.get("customer_safe_answer")

        available_evidence = [item for item in evidence if item.get("status") == "available"]
        external_assurance = [
            item
            for item in response.get("external_assurance", [])
            if item.get("status") == "available"
        ]

        if answer in {"yes", "partial"} and not available_evidence:
            blockers.append(f"{response_id}: affirmative answer lacks available evidence")

        if answer in {"yes", "partial"} and not customer_safe_answer:
            blockers.append(f"{response_id}: affirmative answer lacks customer-safe wording")

        if answer == "needs_review":
            blockers.append(f"{response_id}: unresolved review route")

        if review.get("status") == "approved" and not review.get("reviewer"):
            blockers.append(f"{response_id}: approved response lacks reviewer")

        if claim_strength in {"independently_assessed", "certified"} and not external_assurance:
            blockers.append(
                f"{response_id}: {claim_strength} claim lacks available external assurance"
            )

        if any(item.get("status") == "pending" for item in evidence):
            warnings.append(f"{response_id}: evidence is pending")

    return TrustCheck(
        ready=not blockers,
        blockers=tuple(sorted(set(blockers))),
        warnings=tuple(sorted(set(warnings))),
    )


def evaluate_exception_register(document: dict[str, Any]) -> TrustCheck:
    blockers: list[str] = []
    warnings: list[str] = []

    for item in document.get("exceptions", []):
        exception_id = item.get("id", "<unknown>")
        opened_at = _parse_date(item.get("opened_at"))
        due_at = _parse_date(item.get("due_at"))
        closed_at = _parse_date(item.get("closed_at"))
        risk_acceptance = item.get("risk_acceptance")
        status = item.get("status")

        if due_at and opened_at and due_at < opened_at:
            blockers.append(f"{exception_id}: due date precedes opened date")

        if closed_at and opened_at and closed_at < opened_at:
            blockers.append(f"{exception_id}: closed date precedes opened date")

        if status == "risk_accepted":
            if not isinstance(risk_acceptance, dict):
                blockers.append(f"{exception_id}: risk acceptance metadata is missing")
            else:
                expires_at = _parse_date(risk_acceptance.get("expires_at"))
                if expires_at and opened_at and expires_at < opened_at:
                    blockers.append(
                        f"{exception_id}: risk acceptance expiry precedes opened date"
                    )

        if status in {"open", "remediating"} and item.get("severity") in {"critical", "high"}:
            warnings.append(f"{exception_id}: material exception remains {status}")

    return TrustCheck(
        ready=not blockers,
        blockers=tuple(sorted(set(blockers))),
        warnings=tuple(sorted(set(warnings))),
    )


def summarize_customer_trust(
    questionnaire: dict[str, Any],
    exception_register: dict[str, Any],
) -> dict[str, Any]:
    questionnaire_check = evaluate_questionnaire(questionnaire)
    exception_check = evaluate_exception_register(exception_register)

    counts: dict[str, int] = {}
    for response in questionnaire.get("responses", []):
        answer = response.get("answer", "unknown")
        counts[answer] = counts.get(answer, 0) + 1

    return {
        "schema_version": "1.0",
        "ready_for_customer_use": questionnaire_check.ready and exception_check.ready,
        "questionnaire": {
            "answer_counts": dict(sorted(counts.items())),
            "blockers": list(questionnaire_check.blockers),
            "warnings": list(questionnaire_check.warnings),
        },
        "exceptions": {
            "count": len(exception_register.get("exceptions", [])),
            "blockers": list(exception_check.blockers),
            "warnings": list(exception_check.warnings),
        },
        "non_claims": [
            "Readiness only evaluates repository reference rules.",
            "This output is not customer approval, certification or legal advice.",
        ],
    }


def _parse_date(value: Any) -> date | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
