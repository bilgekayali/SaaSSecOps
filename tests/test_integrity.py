import hashlib
import json
import unittest
from pathlib import Path

from saassecops.integrity import (
    IntegrityError,
    build_envelope,
    sign_envelope,
    verify_envelope,
    verify_payload_binding,
)


ROOT = Path(__file__).resolve().parents[1]
TEST_SEED = hashlib.sha256(b"SaaSSecOps v0.7 synthetic test-only Ed25519 key").digest()
REVOKED_SEED = hashlib.sha256(b"SaaSSecOps v0.7 revoked synthetic Ed25519 key").digest()


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "examples" / "evidence-payload.json").read_text(encoding="utf-8"))
        self.registry = json.loads((ROOT / "examples" / "key-registry.json").read_text(encoding="utf-8"))

    def envelope(self, key_id="test-ed25519-2026-01", seed=TEST_SEED):
        envelope = build_envelope(
            payload=self.payload,
            payload_type="synthetic-control-evidence",
            source_sha="1" * 40,
            key_id=key_id,
            issued_at="2026-09-01T00:00:00Z",
            revalidate_after="2026-09-15T00:00:00Z",
            expires_at="2026-10-01T00:00:00Z",
        )
        return sign_envelope(envelope, seed)

    def test_valid_signature_payload_binding_and_freshness_states(self):
        envelope = self.envelope()
        verify_payload_binding(self.payload, envelope)
        self.assertEqual(verify_envelope(envelope, self.registry, observed_at="2026-09-10T00:00:00Z")["freshness"], "current")
        self.assertEqual(verify_envelope(envelope, self.registry, observed_at="2026-09-20T00:00:00Z")["freshness"], "revalidation_due")
        self.assertEqual(verify_envelope(envelope, self.registry, observed_at="2026-10-02T00:00:00Z")["freshness"], "expired")

    def test_envelope_tampering_is_rejected(self):
        envelope = self.envelope()
        envelope["source"]["git_sha"] = "2" * 40
        with self.assertRaises(IntegrityError):
            verify_envelope(envelope, self.registry, observed_at="2026-09-10T00:00:00Z")

    def test_payload_tampering_is_rejected(self):
        envelope = self.envelope()
        modified = json.loads(json.dumps(self.payload))
        modified["statement"] = "modified statement"
        with self.assertRaises(IntegrityError):
            verify_payload_binding(modified, envelope)

    def test_revoked_key_is_rejected(self):
        envelope = self.envelope("test-ed25519-revoked", REVOKED_SEED)
        with self.assertRaises(IntegrityError):
            verify_envelope(envelope, self.registry, observed_at="2026-09-10T00:00:00Z")

    def test_signature_is_deterministic_for_same_key_and_envelope(self):
        first = self.envelope()
        second = self.envelope()
        self.assertEqual(first["signature"]["value_b64"], second["signature"]["value_b64"])


if __name__ == "__main__":
    unittest.main()
