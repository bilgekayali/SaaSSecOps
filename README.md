# SaaSSecOps

**AWS SaaS Security & Trust Reference Architecture**

SaaSSecOps is an open-source reference architecture and local assurance toolkit for multi-tenant SaaS security on AWS. It connects tenant isolation, application/API security, software supply-chain controls, customer-trust workflows, evidence integrity and stable machine-readable contracts in one inspectable project.

> [!IMPORTANT]
> This repository is a **reference architecture and portfolio demonstration**. It does not prove that any AWS environment or SaaS application has been deployed, independently assessed, penetration tested, certified or approved for production.

Current package milestone: **v0.9.0 — v1 Release Candidate**.

## Summary

v0.9 is the release-candidate hardening pass. The v1 public-contract candidate from v0.8 remains unchanged while the repository is tested as a distributable package from one exact source revision. CI now includes clean wheel installation outside the source tree, CLI smoke testing, exact-source release evidence, a machine-readable release checklist, repository blocker register and expanded threat-model review.

The frozen v1 candidate fingerprint remains:

`sha256:d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

## Release-candidate boundary

The candidate keeps the existing public surface:

- `saassecops assess <posture> --policy <policy> [--output ...] [--manifest-output ...]`
- `saassecops validate <document> --kind <public-contract-kind>`
- `saassecops digest <document>`
- `saassecops contract-snapshot`
- `saassecops --version`
- the current public JSON Schema identities;
- deterministic assessment identity semantics;
- exact-byte SHA-256 digest semantics;
- evidence-manifest source/report binding semantics;
- fail-closed handling for unsupported contract kinds and future schema versions.

The checked descriptor is [contracts/v1-candidate.json](contracts/v1-candidate.json), with its digest in [contracts/v1-candidate.sha256](contracts/v1-candidate.sha256).

## v0.9 release gates

The release-candidate review requires:

- Python 3.11–3.13 tests;
- stable-contract fingerprint verification;
- all public contract validations;
- tenant-isolation negative vectors;
- customer-trust fail-closed checks;
- evidence signature, payload-binding, freshness and revocation gates;
- CycloneDX 1.7 SBOM generation and verification;
- strict dependency vulnerability audit;
- package build;
- **clean wheel install in an isolated virtual environment**;
- CLI smoke tests executed outside the checkout;
- exact-source release manifest;
- both Terraform roots validated using Terraform 1.16.0;
- CodeQL on the same candidate SHA;
- repository-owned critical/high blocker gate.

See [v1 Release Candidate Review](docs/RELEASE_CANDIDATE_REVIEW.md).

## Security and evidence layers

- AWS multi-account security/logging reference with delegated administration.
- Pool, silo and bridge tenant-isolation contracts with negative cross-tenant tests.
- OWASP Top 10:2025 and OWASP API Security Top 10:2023 mappings.
- CodeQL, dependency audit and CycloneDX 1.7 SBOM gates.
- Vulnerability finding and time-bounded exception evidence.
- Evidence-bound security-questionnaire and Security GTM control model.
- Customer-facing assurance pack and trust-exception register.
- Ed25519 evidence envelopes with payload/source binding.
- Active/retired/revoked signing-key lifecycle and fail-closed revocation checks.
- `current`, `revalidation_due` and `expired` evidence decisions.
- Exact-source release manifest and release-evidence bundle.
- Stable contract descriptor/fingerprint and explicit compatibility policy.

## Quickstart

```bash
python -m pip install -e .
python scripts/verify_stable_contract.py
python scripts/verify_release_candidate.py \
  --source-sha 0000000000000000000000000000000000000000 \
  --output artifacts/v1-rc-review.json
```

The zero SHA above is only a local structural example. CI supplies the exact GitHub candidate SHA.

Run repository tests:

```bash
python -m unittest discover -s tests -v
```

## Compatibility

Compatibility policy is defined in [COMPATIBILITY.md](COMPATIBILITY.md). Migration guidance for consumers preparing for v1 is in [Migration to v1](docs/MIGRATION_TO_V1.md).

Reference Terraform, diagrams, documentation prose, release-engineering scripts and internal Python modules remain non-API surfaces unless explicitly promoted.

## Key-management boundary

No production private signing key is committed to this repository. CI uses deterministic synthetic test-only Ed25519 material for reproducible verification. Real private keys belong in an approved external signing boundary such as an HSM, KMS or protected signing service.

## Release direction

v0.9 is intended to be the final pre-v1 candidate. v1.0 should promote the already verified stable contract rather than introduce a new feature set. See [ROADMAP.md](ROADMAP.md).

## Explicit non-claims

SaaSSecOps does **not** establish deployed security effectiveness, production key custody, vulnerability absence, penetration-test success, certification, regulatory compliance, contractual acceptance or customer approval. Release-candidate status, cryptographic verification and a stable contract fingerprint prove repository quality/integrity properties only; they do not prove the truth or operational effectiveness of underlying security claims.

## Author

Bilge Kayalı

## License

Apache License 2.0.
