import json
import unittest
from pathlib import Path

from saassecops.cli import build_parser
from saassecops.stable_contract import contract_fingerprint, stable_contract_descriptor


ROOT = Path(__file__).resolve().parents[1]


class StableContractTests(unittest.TestCase):
    def test_generated_contract_matches_checked_candidate(self):
        expected = json.loads((ROOT / "contracts" / "v1-candidate.json").read_text(encoding="utf-8"))
        actual = stable_contract_descriptor(build_parser())
        self.assertEqual(actual, expected)

    def test_candidate_fingerprint_matches_checked_digest(self):
        expected = (ROOT / "contracts" / "v1-candidate.sha256").read_text(encoding="utf-8").strip()
        actual = contract_fingerprint(stable_contract_descriptor(build_parser()))
        self.assertEqual(actual, expected)

    def test_schema_identities_are_unique_and_project_scoped(self):
        contract = stable_contract_descriptor(build_parser())
        identities = list(contract["schemas"].values())
        self.assertEqual(len(identities), len(set(identities)))
        for identity in identities:
            self.assertTrue(identity.startswith("https://"))
            self.assertIn("bilgekayali", identity)
            self.assertIn("/SaaSSecOps/schemas/", identity)


if __name__ == "__main__":
    unittest.main()
