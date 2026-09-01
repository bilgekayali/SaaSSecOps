import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from saassecops.contracts import ContractError, validate_document
from saassecops.evaluator import load_json

ROOT = Path(__file__).resolve().parents[1]


class AppSecReferenceTests(unittest.TestCase):
    def test_appsec_reference_contract(self):
        document = load_json(ROOT / "architecture" / "appsec-reference.json")
        validate_document(document, "appsec")
        self.assertEqual(len(document["standards"]["owasp_top10"]["risks"]), 10)
        self.assertEqual(len(document["standards"]["owasp_api_security_top10"]["risks"]), 10)
        self.assertEqual(document["supply_chain"]["cyclonedx_version"], "1.7")

    def test_vulnerability_reference_requires_exception_for_risk_acceptance(self):
        document = load_json(ROOT / "examples" / "vulnerability-evidence.json")
        validate_document(document, "vulnerability-evidence")
        invalid = json.loads(json.dumps(document))
        invalid["findings"][1].pop("exception")
        with self.assertRaises(ContractError):
            validate_document(invalid, "vulnerability-evidence")

    def test_cyclonedx_sbom_generation_and_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "saassecops.cdx.json"
            subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_sbom.py"), "--output", str(output)], check=True)
            subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_sbom.py"), str(output)], check=True)
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(document["specVersion"], "1.7")
            self.assertTrue(any(component["name"].lower() == "jsonschema" for component in document["components"]))


if __name__ == "__main__":
    unittest.main()
