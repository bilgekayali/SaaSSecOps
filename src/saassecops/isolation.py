from __future__ import annotations

import re
from typing import Iterable

TENANT_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


class IsolationError(ValueError):
    """Raised when a tenant context is malformed."""


def _tenant(value: str | None) -> str | None:
    if value is None:
        return None
    if not TENANT_ID.fullmatch(value):
        raise IsolationError(
            "tenant identifiers must match ^[a-z0-9][a-z0-9-]{0,62}$"
        )
    return value


def evaluate_tenant_access(
    *,
    principal_tenant: str | None,
    resource_tenant: str | None,
    action: str,
    allowed_actions: Iterable[str],
) -> dict[str, str]:
    """Evaluate SaaSSecOps tenant-boundary invariants.

    This is a deterministic reference decision, not an AWS IAM policy simulator.
    """
    principal = _tenant(principal_tenant)
    resource = _tenant(resource_tenant)
    allowed = frozenset(allowed_actions)

    if not action:
        raise IsolationError("action must be non-empty")

    if principal is None:
        return {"decision": "deny", "reason": "missing_principal_tenant"}

    if resource is None:
        return {"decision": "deny", "reason": "missing_resource_tenant"}

    if action not in allowed:
        return {"decision": "deny", "reason": "action_not_allowed"}

    if principal != resource:
        return {"decision": "deny", "reason": "cross_tenant_denied"}

    return {"decision": "allow", "reason": "tenant_and_action_match"}


def run_vectors(reference: dict[str, object]) -> list[dict[str, str]]:
    """Run the declared synthetic isolation vectors and return their outcomes."""
    vectors = reference.get("test_vectors")
    if not isinstance(vectors, list):
        raise IsolationError("reference.test_vectors must be a list")

    outcomes: list[dict[str, str]] = []
    for vector in vectors:
        if not isinstance(vector, dict):
            raise IsolationError("every test vector must be an object")
        result = evaluate_tenant_access(
            principal_tenant=vector.get("principal_tenant"),
            resource_tenant=vector.get("resource_tenant"),
            action=str(vector.get("action", "")),
            allowed_actions=vector.get("allowed_actions", []),
        )
        expected = vector.get("expected")
        outcomes.append(
            {
                "id": str(vector.get("id", "")),
                "expected": str(expected),
                "actual": result["decision"],
                "reason": result["reason"],
            }
        )
    return outcomes
