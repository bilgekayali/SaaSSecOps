from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


class IntegrityError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_sha256(payload: Any) -> str:
    return sha256_hex(canonical_json_bytes(payload))


def verify_payload_binding(payload: Any, envelope: dict[str, Any]) -> None:
    expected = envelope.get("payload_sha256")
    actual = payload_sha256(payload)
    if expected != actual:
        raise IntegrityError("payload digest does not match evidence envelope")


def _parse_timestamp(value: str) -> datetime:
    text = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise IntegrityError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def validate_key_registry_semantics(registry: dict[str, Any]) -> None:
    seen: set[str] = set()
    for key in registry.get("keys", []):
        key_id = key.get("key_id", "")
        if key_id in seen:
            raise IntegrityError(f"duplicate key_id: {key_id}")
        seen.add(key_id)

        valid_from = _parse_timestamp(key["valid_from"])
        valid_until = _parse_timestamp(key["valid_until"]) if key.get("valid_until") else None
        if valid_until and valid_until < valid_from:
            raise IntegrityError(f"key {key_id} has invalid validity window")

        if key.get("status") == "revoked":
            if not key.get("revoked_at") or not key.get("revocation_reason"):
                raise IntegrityError(f"revoked key {key_id} requires revocation metadata")
        elif key.get("revoked_at") or key.get("revocation_reason"):
            raise IntegrityError(f"non-revoked key {key_id} cannot carry revocation metadata")


def _key_record(registry: dict[str, Any], key_id: str) -> dict[str, Any]:
    validate_key_registry_semantics(registry)
    for record in registry.get("keys", []):
        if record.get("key_id") == key_id:
            return record
    raise IntegrityError(f"unknown key_id: {key_id}")


def build_envelope(
    *,
    payload: Any,
    payload_type: str,
    source_sha: str,
    key_id: str,
    issued_at: str,
    revalidate_after: str,
    expires_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "payload_type": payload_type,
        "payload_sha256": payload_sha256(payload),
        "source": {"repository": "bilgekayali/SaaSSecOps", "git_sha": source_sha},
        "freshness": {
            "issued_at": issued_at,
            "revalidate_after": revalidate_after,
            "expires_at": expires_at,
        },
        "signature": {"algorithm": "Ed25519", "key_id": key_id, "value_b64": ""},
    }


def _unsigned_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    unsigned = json.loads(json.dumps(envelope))
    unsigned["signature"]["value_b64"] = ""
    return unsigned


def sign_envelope(envelope: dict[str, Any], private_key_raw: bytes) -> dict[str, Any]:
    if len(private_key_raw) != 32:
        raise IntegrityError("Ed25519 private key seed must be 32 raw bytes")
    signed = json.loads(json.dumps(envelope))
    message = canonical_json_bytes(_unsigned_envelope(signed))
    signature = Ed25519PrivateKey.from_private_bytes(private_key_raw).sign(message)
    signed["signature"]["value_b64"] = base64.b64encode(signature).decode("ascii")
    return signed


def verify_envelope(
    envelope: dict[str, Any],
    registry: dict[str, Any],
    *,
    observed_at: str,
) -> dict[str, Any]:
    signature = envelope.get("signature", {})
    if signature.get("algorithm") != "Ed25519":
        raise IntegrityError("unsupported signature algorithm")

    key = _key_record(registry, signature.get("key_id", ""))
    if key.get("algorithm") != "Ed25519":
        raise IntegrityError("key algorithm mismatch")
    if key.get("status") == "revoked":
        raise IntegrityError("signing key is revoked")

    issued = _parse_timestamp(envelope["freshness"]["issued_at"])
    valid_from = _parse_timestamp(key["valid_from"])
    valid_until = _parse_timestamp(key["valid_until"]) if key.get("valid_until") else None
    if issued < valid_from or (valid_until and issued > valid_until):
        raise IntegrityError("signing key was outside its signing-validity window")

    try:
        public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(key["public_key_b64"], validate=True))
        public_key.verify(
            base64.b64decode(signature.get("value_b64", ""), validate=True),
            canonical_json_bytes(_unsigned_envelope(envelope)),
        )
    except (ValueError, InvalidSignature) as exc:
        raise IntegrityError("evidence signature verification failed") from exc

    freshness = evaluate_freshness(envelope["freshness"], observed_at=observed_at)
    return {
        "signature_valid": True,
        "key_id": key["key_id"],
        "key_status": key["status"],
        "freshness": freshness,
    }


def evaluate_freshness(freshness: dict[str, Any], *, observed_at: str) -> str:
    observed = _parse_timestamp(observed_at)
    issued = _parse_timestamp(freshness["issued_at"])
    revalidate_after = _parse_timestamp(freshness["revalidate_after"])
    expires_at = _parse_timestamp(freshness["expires_at"])
    if not (issued <= revalidate_after <= expires_at):
        raise IntegrityError("freshness timestamps must be monotonic")
    if observed > expires_at:
        return "expired"
    if observed > revalidate_after:
        return "revalidation_due"
    return "current"
