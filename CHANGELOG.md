# Changelog

## 0.8.0

- Added a checked v1 public-contract candidate derived from the actual argparse command surface and public JSON Schema identities.
- Added a canonical SHA-256 contract fingerprint and CI drift detection across Python 3.11–3.13.
- Added stable-contract semantic invariants for assessment identity, exact-byte digests, evidence binding and fail-closed future-contract handling.
- Added explicit SemVer compatibility rules for the candidate boundary.
- Added migration guidance for consumers preparing for v1.
- Added the stable contract descriptor and fingerprint to the release-evidence bundle.

## 0.7.0

- Added Ed25519 signed evidence envelopes bound to canonical payload digests and exact Git source revisions.
- Added public signing-key lifecycle registry with active, retired and revoked states.
- Added fail-closed verification for tampering and revoked signing keys.
- Added explicit evidence freshness decisions: `current`, `revalidation_due` and `expired`.
- Added exact-source release manifests with SHA-256 checksums for distributions and CycloneDX SBOM.
- Added CI release-evidence bundle generation and tagged build-provenance workflow.
- Added synthetic deterministic signing tests without committing production private-key material.
- Expanded the public contract snapshot with evidence-envelope, key-registry and release-manifest schemas.

## 0.6.0

- Added evidence-bound security-questionnaire response contracts.
- Added customer trust architecture and machine-readable Security GTM responsibility model.
- Added customer-facing security assurance pack guidance.
- Added penetration-test/audit/security-review exception register contract.
- Added fail-closed trust checks for unsupported affirmative, independent-assessment and certification claims.
- Added a deterministic customer-trust summary with intentional `needs_review` reference scenarios.
- Expanded CI and the public contract snapshot with customer-trust schemas.

## 0.5.0

- Added OWASP Top 10:2025 and API Security Top 10:2023 application/API security references.
- Added CodeQL, dependency audit and CycloneDX 1.7 SBOM gates.
- Added vulnerability finding/exception evidence with time-bounded risk acceptance.

## 0.4.0

- Added pool, silo and bridge tenant-isolation patterns and fail-closed negative vectors.
- Added AWS STS/ABAC pooled authorization reference.

## 0.3.0

- Added AWS multi-account security topology, delegated administration and SCP references.

## 0.2.0

- Added strict contracts, deterministic evidence identity, CI/package/Terraform gates and v1 roadmap.

## 0.1.0

- Initial AWS SaaS security and trust reference architecture.
