# Changelog

## 1.0.0

- Promoted the verified v0.9 release candidate to the stable public boundary.
- Retained the v0.8/v0.9 stable-contract fingerprint unchanged.
- Added a machine-readable v1 stable release checklist and exact-source stable release verifier.
- Added explicit RC-to-v1 contract continuity checks.
- Added stable release documentation and final SemVer compatibility language.
- Updated CI to build, clean-install and smoke-test the 1.0.0 wheel, generate exact-source release evidence and produce a stable-release review artifact.
- Updated the tagged release-evidence workflow to verify v1.0.0 and emit build provenance from the exact tagged source.
- Preserved the existing non-claims: stable status is not proof of deployment, penetration-test success, compliance, certification, independent assurance or customer acceptance.

## 0.9.0

- Added v1 release-candidate review and machine-readable checklist.
- Added clean wheel installation and CLI smoke tests outside the source checkout.
- Expanded the threat model across cloud, tenant, AppSec/API, supply-chain, customer-trust, evidence-integrity and incident-response domains.
- Added a repository-owned blocker register that fails the release review on known open critical/high defects.
- Added exact-SHA release-candidate review artifacts to the CI evidence bundle.
- Pinned critical GitHub Actions to reviewed commit SHAs and moved CodeQL to v4.
- Pinned Terraform validation to stable Terraform 1.16.0.
- Retained the v0.8 stable public-contract fingerprint unchanged.

## 0.8.0

- Added an argparse-derived v1 public-contract candidate.
- Added a checked contract descriptor and canonical SHA-256 fingerprint.
- Added CI drift detection for CLI/schema identities and core evidence semantics.
- Formalized SemVer compatibility rules and v0.x-to-v1 migration guidance.
- Added the stable candidate descriptor/fingerprint to release evidence.

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
