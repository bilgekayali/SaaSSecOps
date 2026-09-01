import json
import unittest
from pathlib import Path

from saassecops.contracts import validate_document
from saassecops.isolation import IsolationError, evaluate_tenant_access, run_vectors

ROOT = Path(__file__).resolve().parents[1]


class TenantIsolationTests(unittest.TestCase):
    def setUp(self):
        self.reference = json.loads(
            (ROOT / "architecture" / "tenant-isolation-reference.json").read_text(
                encoding="utf-8"
            )
        )

    def test_reference_contract_is_valid(self):
        validate_document(self.reference, "tenant-isolation")

    def test_all_declared_vectors_match(self):
        outcomes = run_vectors(self.reference)
        self.assertTrue(outcomes)
        self.assertEqual(
            [(item["id"], item["actual"]) for item in outcomes],
            [(item["id"], item["expected"]) for item in outcomes],
        )

    def test_cross_tenant_access_is_denied(self):
        result = evaluate_tenant_access(
            principal_tenant="tenant-a",
            resource_tenant="tenant-b",
            action="read",
            allowed_actions=["read"],
        )
        self.assertEqual(result, {"decision": "deny", "reason": "cross_tenant_denied"})

    def test_missing_context_fails_closed(self):
        result = evaluate_tenant_access(
            principal_tenant=None,
            resource_tenant="tenant-a",
            action="read",
            allowed_actions=["read"],
        )
        self.assertEqual(
            result, {"decision": "deny", "reason": "missing_principal_tenant"}
        )

    def test_disallowed_action_fails_closed(self):
        result = evaluate_tenant_access(
            principal_tenant="tenant-a",
            resource_tenant="tenant-a",
            action="delete",
            allowed_actions=["read", "write"],
        )
        self.assertEqual(result, {"decision": "deny", "reason": "action_not_allowed"})

    def test_malformed_tenant_is_rejected(self):
        with self.assertRaises(IsolationError):
            evaluate_tenant_access(
                principal_tenant="../tenant-a",
                resource_tenant="tenant-a",
                action="read",
                allowed_actions=["read"],
            )

    def test_pool_policy_uses_principal_tenant_tag(self):
        policy = json.loads(
            (ROOT / "policies" / "iam" / "pool-s3-tenant-prefix-policy.json").read_text(
                encoding="utf-8"
            )
        )
        rendered = json.dumps(policy)
        self.assertIn("${aws:PrincipalTag/tenant-id}", rendered)
        self.assertIn("s3:prefix", rendered)


if __name__ == "__main__":
    unittest.main()
