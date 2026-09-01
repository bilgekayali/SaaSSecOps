from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from saassecops.contracts import validate_document
from saassecops.integrity import (
    IntegrityError,
    build_envelope,
    sign_envelope,
    verify_envelope,
    verify_payload_binding,
)


TEST_KEY_ID = "test-ed25519-2026-01"
TEST_KEY_SEED = hashlib.sha256(b"SaaSSecOps v0.7 synthetic test-only Ed25519 key").digest()
REVOKED_KEY_SEED = hashlib.sha256(b"SaaSSecOps v0.7 revoked synthetic Ed25519 key").digest()


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", default="examples/evidence-payload.json")
    parser.add_argument("--registry", default="examples/key-registry.json")
    parser.add_argument("--output", default="artifacts/evidence-envelope.json")
    parser.add_argument("--summary-output", default="artifacts/evidence-integrity-summary.json")
    args = parser.parse_args()

    payload = _load(args.payload)
    registry = _load(args.registry)
    validate_document(registry, "key-registry")

    source_sha = os.environ.get("SAASSECOPS_SOURCE_SHA") or os.environ.get("GITHUB_SHA", "0" * 40)
    if len(source_sha) != 40 or any(ch not in "0123456789abcdef" for ch in source_sha.lower()):
        raise SystemExit("evidence source SHA must be a 40-character hexadecimal commit SHA")

    envelope = build_envelope(
        payload=payload,
        payload_type="synthetic-control-evidence",
        source_sha=source_sha.lower(),
        key_id=TEST_KEY_ID,
        issued_at="2026-09-01T00:00:00Z",
        revalidate_after="2026-09-15T00:00:00Z",
        expires_at="2026-10-01T00:00:00Z",
    )
    envelope = sign_envelope(envelope, TEST_KEY_SEED)
    validate_document(envelope, "evidence-envelope")
    verify_payload_binding(payload, envelope)

    current = verify_envelope(envelope, registry, observed_at="2026-09-10T00:00:00Z")
    revalidation_due = verify_envelope(envelope, registry, observed_at="2026-09-20T00:00:00Z")
    expired = verify_envelope(envelope, registry, observed_at="2026-10-02T00:00:00Z")

    tampered = json.loads(json.dumps(envelope))
    tampered["payload_sha256"] = "0" * 64
    envelope_tamper_rejected = False
    try:
        verify_envelope(tampered, registry, observed_at="2026-09-10T00:00:00Z")
    except IntegrityError:
        envelope_tamper_rejected = True

    modified_payload = json.loads(json.dumps(payload))
    modified_payload["statement"] = "tampered synthetic statement"
    payload_tamper_rejected = False
    try:
        verify_payload_binding(modified_payload, envelope)
    except IntegrityError:
        payload_tamper_rejected = True

    revoked_envelope = build_envelope(
        payload=payload,
        payload_type="synthetic-control-evidence",
        source_sha=source_sha.lower(),
        key_id="test-ed25519-revoked",
        issued_at="2026-09-01T00:00:00Z",
        revalidate_after="2026-09-15T00:00:00Z",
        expires_at="2026-10-01T00:00:00Z",
    )
    revoked_envelope = sign_envelope(revoked_envelope, REVOKED_KEY_SEED)
    revoked_rejected = False
    try:
        verify_envelope(revoked_envelope, registry, observed_at="2026-09-10T00:00:00Z")
    except IntegrityError:
        revoked_rejected = True

    if current["freshness"] != "current":
        raise SystemExit("expected current evidence")
    if revalidation_due["freshness"] != "revalidation_due":
        raise SystemExit("expected revalidation_due evidence")
    if expired["freshness"] != "expired":
        raise SystemExit("expected expired evidence")
    if not envelope_tamper_rejected or not payload_tamper_rejected or not revoked_rejected:
        raise SystemExit("negative integrity test did not fail closed")

    summary = {
        "schema_version": "1.0",
        "source_sha": source_sha.lower(),
        "signature_valid": current["signature_valid"],
        "current_status": current["freshness"],
        "revalidation_status": revalidation_due["freshness"],
        "expired_status": expired["freshness"],
        "envelope_tamper_rejected": envelope_tamper_rejected,
        "payload_tamper_rejected": payload_tamper_rejected,
        "revoked_key_rejected": revoked_rejected,
        "private_key_persisted": False,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.summary_output).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
