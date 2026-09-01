# Evidence Signing Key Lifecycle

## States

The reference registry supports three states:

- `active` — accepted for verification inside its validity window;
- `retired` — no longer intended for new signatures but retained as historical metadata;
- `revoked` — rejected by the verifier regardless of signature correctness.

## Registry metadata

Each key record carries:

- stable `key_id`;
- algorithm (`Ed25519` in v0.7);
- raw public key encoded as Base64;
- lifecycle status;
- validity start/end;
- optional revocation timestamp and reason;
- declared scope.

Private keys are not part of the registry schema and must not be committed to the repository.

## Rotation reference

A production rotation process should:

1. create a new key in the external signing boundary;
2. publish its public key with a new `key_id` and future/active validity window;
3. move new signing operations to the new key;
4. retain the previous public key for historical verification;
5. retire or revoke the previous key according to policy;
6. preserve an auditable record of the lifecycle change.

## Revocation reference

Revocation is fail-closed. Once a key is marked `revoked`, SaaSSecOps verification rejects envelopes signed by it even when the mathematical signature is otherwise valid.

A real organization should define emergency revocation authority, notification/escalation paths, affected-evidence identification and mandatory re-signing/revalidation rules.

## Reference boundary

The repository demonstrates verification semantics and lifecycle metadata only. It does not establish production key custody, operator separation, HSM/KMS configuration, compromise detection or cryptographic certification.
