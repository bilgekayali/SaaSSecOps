import json
import unittest
from pathlib import Path

from saassecops.cli import build_parser
from saassecops.stable_contract import contract_fingerprint, stable_contract_descriptor


ROOT = Path(__file__).resolve().parents[1]


class ReleaseCandidateHistoryTests(unittest.TestCase):
    def setUp(self):
        self.checklist = json.loads((ROOT / "release" / "v1-rc-checklist.json").read_text(encoding="utf-8"))
        self.defects = json.loads((ROOT / "release" / "defect-register.json").read_text(encoding="utf-8"))

    def test_checked_rc_contract_remains_intact(self):
        self.assertEqual(self.checklist["candidate_version"], "0.9.0")
        checked = (ROOT / "contracts" / "v1-candidate.sha256").read_text(encoding="utf-8").strip()
        actual = contract_fingerprint(stable_contract_descriptor(build_parser()))
        self.assertEqual(checked, self.checklist["stable_contract_sha256"])
        self.assertEqual(actual, checked)

    def test_rc_required_documents_remain_available(self):
        missing = [path for path in self.checklist["required_documents"] if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_no_known_repository_high_or_critical_blocker(self):
        blockers = [
            entry for entry in self.defects["entries"]
            if entry.get("severity") in {"critical", "high"}
            and entry.get("status") in {"open", "accepted_for_fix"}
        ]
        self.assertEqual(blockers, [])


if __name__ == "__main__":
    unittest.main()
