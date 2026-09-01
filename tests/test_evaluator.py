import unittest
from pathlib import Path

from saassecops.evaluator import assess, load_json

ROOT = Path(__file__).resolve().parents[1]


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_json(ROOT / "policies" / "aws-saas-controls.json")

    def test_reference_passes(self):
        report = assess(load_json(ROOT / "examples" / "reference-architecture.json"), self.policy)
        self.assertEqual(report["overall"], "pass")
        self.assertEqual(report["summary"]["gap"], 0)
        self.assertEqual(report["summary"]["pass"], 26)

    def test_risky_exposes_gaps(self):
        report = assess(load_json(ROOT / "examples" / "risky-architecture.json"), self.policy)
        gaps = {r["id"] for r in report["results"] if r["status"] == "gap"}
        self.assertEqual(report["overall"], "with_gaps")
        self.assertTrue({"TENANT-03", "NET-02", "LOG-02", "DET-01", "TRUST-02"}.issubset(gaps))

    def test_digests_stable(self):
        posture = load_json(ROOT / "examples" / "reference-architecture.json")
        a, b = assess(posture, self.policy), assess(posture, self.policy)
        self.assertEqual(a["input_sha256"], b["input_sha256"])
        self.assertEqual(a["policy_sha256"], b["policy_sha256"])


if __name__ == "__main__":
    unittest.main()
