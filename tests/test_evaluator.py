import json
import unittest
from pathlib import Path

from saassecops.contracts import ContractError, contract_snapshot, validate_document
from saassecops.evaluator import assess, build_evidence_manifest, load_json

ROOT = Path(__file__).resolve().parents[1]


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_json(ROOT / "policies" / "aws-saas-controls.json")
        self.posture = load_json(ROOT / "examples" / "reference-architecture.json")

    def test_reference_passes(self):
        report = assess(self.posture, self.policy)
        self.assertEqual(report["overall"], "pass")
        self.assertEqual(report["summary"]["gap"], 0)
        self.assertEqual(report["summary"]["pass"], 26)
        validate_document(report, "report")

    def test_risky_exposes_gaps(self):
        report = assess(load_json(ROOT / "examples" / "risky-architecture.json"), self.policy)
        gaps = {r["id"] for r in report["results"] if r["status"] == "gap"}
        self.assertEqual(report["overall"], "with_gaps")
        self.assertTrue({"TENANT-03", "NET-02", "LOG-02", "DET-01", "TRUST-02"}.issubset(gaps))

    def test_assessment_identity_is_stable(self):
        first = assess(self.posture, self.policy)
        second = assess(self.posture, self.policy)
        self.assertEqual(first["assessment_id"], second["assessment_id"])
        self.assertEqual(first["input_sha256"], second["input_sha256"])
        self.assertEqual(first["policy_sha256"], second["policy_sha256"])

    def test_contract_rejects_unknown_posture_field(self):
        posture = json.loads(json.dumps(self.posture))
        posture["unexpected"] = True
        with self.assertRaises(ContractError):
            validate_document(posture, "posture")

    def test_manifest_binds_exact_report_bytes(self):
        report = assess(self.posture, self.policy)
        report_bytes = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
        manifest = build_evidence_manifest(
            report,
            posture_name="examples/reference-architecture.json",
            policy_name="policies/aws-saas-controls.json",
            report_name="artifacts/reference-assessment.json",
            report_bytes=report_bytes,
        )
        validate_document(manifest, "manifest")
        self.assertEqual(manifest["assessment_id"], report["assessment_id"])
        self.assertEqual(len(manifest["subjects"]["report"]["sha256"]), 64)

    def test_contract_snapshot_has_stable_command_names(self):
        snapshot = contract_snapshot("0.2.0")
        self.assertEqual(snapshot["commands"], ["assess", "contract-snapshot", "digest", "validate"])


if __name__ == "__main__":
    unittest.main()
