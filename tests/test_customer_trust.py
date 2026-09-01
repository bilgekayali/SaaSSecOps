import copy
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from saassecops.contracts import schema_document
from saassecops.trust import evaluate_questionnaire, summarize_customer_trust


def errors(kind, document):
    validator = Draft202012Validator(schema_document(kind), format_checker=FormatChecker())
    return list(validator.iter_errors(document))


class CustomerTrustTests(unittest.TestCase):
    def setUp(self):
        self.approved = {
            "schema_version": "1.0",
            "response_set_id": "approved-reference-set",
            "is_reference_only": True,
            "responses": [{
                "id": "Q-100",
                "question": "Is tenant isolation documented?",
                "answer": "yes",
                "scope": "Reference architecture",
                "owner": "Security Engineering",
                "evidence": [{"id": "E-100", "type": "architecture", "location": "docs/TENANT_ISOLATION.md", "status": "available"}],
                "claim_strength": "documented",
                "review": {"status": "approved", "reviewer": "GRC", "route": None, "notes": None},
                "exceptions": [],
                "customer_safe_answer": "The reference design documents tenant isolation controls.",
                "external_assurance": [],
            }],
            "non_claims": ["Reference-only example."],
        }

    def test_affirmative_answer_requires_evidence(self):
        document = copy.deepcopy(self.approved)
        document["responses"][0]["evidence"] = []
        self.assertTrue(errors("questionnaire", document))

    def test_certification_requires_external_assurance(self):
        document = copy.deepcopy(self.approved)
        document["responses"][0]["claim_strength"] = "certified"
        self.assertTrue(errors("questionnaire", document))

    def test_approved_reference_can_be_ready(self):
        check = evaluate_questionnaire(self.approved)
        self.assertTrue(check.ready)

    def test_needs_review_fails_closed(self):
        document = copy.deepcopy(self.approved)
        item = document["responses"][0]
        item["answer"] = "needs_review"
        item["claim_strength"] = "none"
        item["evidence"] = []
        item["customer_safe_answer"] = None
        item["review"] = {"status": "needs_review", "reviewer": None, "route": "Security Engineering", "notes": "Deployment evidence required."}
        self.assertFalse(evaluate_questionnaire(document).ready)

    def test_risk_acceptance_requires_metadata(self):
        register = {
            "schema_version": "1.0",
            "register_id": "reference-register",
            "is_reference_only": True,
            "exceptions": [{
                "id": "EX-100",
                "source": "audit",
                "title": "Synthetic exception",
                "severity": "low",
                "status": "risk_accepted",
                "owner": "GRC",
                "opened_at": "2026-09-01",
                "due_at": None,
                "closed_at": None,
                "customer_impact": "none_known",
                "disposition": "Temporary reference acceptance.",
                "risk_acceptance": None,
                "evidence_refs": [],
            }],
        }
        self.assertTrue(errors("trust-exceptions", register))

    def test_summary_preserves_customer_readiness_gate(self):
        register = {"schema_version": "1.0", "register_id": "empty-reference-register", "is_reference_only": True, "exceptions": []}
        result = summarize_customer_trust(self.approved, register)
        self.assertTrue(result["ready_for_customer_use"])


if __name__ == "__main__":
    unittest.main()
