# Evidence Integrity

## Scope

v0.7 adds a reference integrity layer around security evidence. The objective is to make four questions explicit and machine-verifiable:

1. What exact payload was asserted?
2. Which exact repository revision produced or referenced it?
3. Which approved signing key signed the envelope?
4. Is the evidence still current, due for revalidation or expired?

This is a repository-level reference. It does not prove production evidence collection, production key custody or independent assurance.

## Evidence envelope

An envelope binds:

- a canonical JSON payload SHA-256;
- a payload type;
- the exact `bilgekayali/SaaSSecOps` Git commit SHA;
- issuance, revalidation and expiry timestamps;
- an Ed25519 key identifier and detached signature value.

The signature covers the complete envelope with the signature value blanked. Changing the payload digest, source revision, freshness metadata or key identifier invalidates verification.

## Freshness decisions

Evidence has three reference states:

- `current` — observed on or before `revalidate_after`;
- `revalidation_due` — past `revalidate_after` but not past `expires_at`;
- `expired` — past `expires_at`.

A valid signature does not make stale evidence current. Cryptographic integrity and evidence currency are separate decisions.

## Release source binding

The release-manifest generator hashes exact distribution bytes and records the exact source commit SHA. The CI evidence bundle includes:

- built distributions;
- CycloneDX 1.7 SBOM;
- exact-source release manifest;
- signed synthetic evidence envelope;
- integrity/freshness negative-test summary.

Tagged releases additionally run the `Release Evidence` workflow, which is configured to request GitHub build-provenance attestation for distribution artifacts.

## Negative gates

CI must reject:

- modified signed-envelope fields;
- signatures from revoked keys;
- malformed key registries or evidence envelopes;
- release manifests not bound to a 40-character source SHA.

The synthetic reference also demonstrates `current`, `revalidation_due` and `expired` states.

## Limitations

The committed test registry contains public keys only. A deterministic synthetic test seed is derived in memory by the test runner so that signature behavior is reproducible. It is public by design and must never be used for production signing.

A real deployment should place private signing material in an approved external key-management boundary such as an HSM, KMS or protected signing service, define operator authorization, rotation and emergency revocation procedures, and preserve independently reviewable audit evidence.
