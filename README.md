# SaaSSecOps

**AWS SaaS Security & Trust Reference Architecture**

SaaSSecOps is an open-source reference architecture and local assurance toolkit for multi-tenant SaaS security on AWS. It connects tenant isolation, application/API security, software supply-chain controls, customer-trust workflows, evidence integrity and stable machine-readable contracts in one inspectable project.

> [!IMPORTANT]
> This repository is a **reference architecture and portfolio demonstration**. It does not prove that any AWS environment or SaaS application has been deployed, independently assessed, penetration tested, certified or approved for production.

Current package version: **v1.0.0 — Stable Security Reference**.

## Summary

v1.0.0 promotes the v0.9 release candidate to the stable public boundary without changing the checked CLI/schema/evidence contract established in v0.8. The release is verified through package tests, fail-closed security vectors, clean wheel installation, exact-source evidence, release blocker review and tagged build provenance.

Stable-contract fingerprint:

`sha256:d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

## Stable public boundary

The v1 boundary includes:

- `saassecops assess <posture> --policy <policy> [--output ...] [--manifest-output ...]`
- `saassecops validate <document> --kind <public-contract-kind>`
- `saassecops digest <document>`
- `saassecops contract-snapshot`
- `saassecops --version`
- the checked public JSON Schema identities;
- deterministic assessment identity semantics;
- exact-byte SHA-256 digest semantics;
- evidence-manifest source/report binding semantics;
- fail-closed handling for unsupported contract kinds and future schema versions.

The frozen descriptor remains [contracts/v1-candidate.json](contracts/v1-candidate.json), with its digest in [contracts/v1-candidate.sha256](contracts/v1-candidate.sha256). The filename is retained to preserve the exact fingerprint verified during the RC-to-v1 promotion.

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
- Stable contract descriptor/fingerprint and explicit SemVer compatibility policy.

## v1.0 release gates

The stable release requires:

- Python 3.11–3.13 tests;
- stable-contract fingerprint verification and RC continuity;
- all public contract validations;
- tenant-isolation negative vectors;
- customer-trust fail-closed checks;
- evidence signature, payload-binding, freshness and revocation gates;
- CycloneDX 1.7 SBOM generation and verification;
- strict dependency vulnerability audit;
- package build plus clean wheel installation outside the checkout;
- CLI smoke testing from the installed wheel;
- exact-source release manifest and stable-release review;
- both Terraform roots validated using Terraform 1.16.0;
- CodeQL on the same source SHA;
- repository-owned critical/high blocker gate;
- `v1.0.0` tag on the verified `main` commit;
- tagged release-evidence workflow and build-provenance attestation.

See [v1.0 Stable Release](docs/STABLE_RELEASE.md).

## Quickstart

```bash
python -m pip install -e .
python scripts/verify_stable_contract.py
python scripts/verify_stable_release.py \
  --source-sha 0000000000000000000000000000000000000000 \
  --output artifacts/v1-stable-review.json
```

The zero SHA is only a local structural example. CI supplies the exact GitHub source SHA.

Run repository tests:

```bash
python -m unittest discover -s tests -v
```

## Compatibility

Compatibility policy is defined in [COMPATIBILITY.md](COMPATIBILITY.md). The v1 stable boundary follows Semantic Versioning; incompatible changes to the checked public surface require a future major version unless a versioned parallel contract is introduced.

Reference Terraform, diagrams, documentation prose, release-engineering scripts and internal Python modules remain non-API surfaces unless explicitly promoted.

## Key-management boundary

No production private signing key is committed to this repository. CI uses deterministic synthetic test-only Ed25519 material for reproducible verification. Real private keys belong in an approved external signing boundary such as an HSM, KMS or protected signing service.

## Explicit non-claims

SaaSSecOps does **not** establish deployed security effectiveness, production key custody, vulnerability absence, penetration-test success, certification, regulatory compliance, contractual acceptance or customer approval. Stable release status, cryptographic verification and a contract fingerprint prove repository compatibility/integrity properties only; they do not prove the truth or operational effectiveness of underlying security claims.

## Author

Bilge Kayalı

## License

Apache License 2.0.
