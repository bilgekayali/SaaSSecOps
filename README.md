# SaaSSecOps

**AWS SaaS Security & Trust Reference Architecture**

SaaSSecOps is an open-source reference architecture and local assurance toolkit for multi-tenant SaaS security on AWS. It connects tenant isolation, application/API security, software supply-chain controls, customer-trust workflows, evidence integrity and stable machine-readable contracts in one inspectable project.

> [!IMPORTANT]
> This repository is a **reference architecture and portfolio demonstration**. It does not prove that any AWS environment or SaaS application has been deployed, independently assessed, penetration tested, certified or approved for production.

Current package milestone: **v0.8.0 — Stable Public Contract Candidate**.

## Summary

v0.8 freezes the first candidate for the v1 public contract. The actual argparse command surface, public JSON Schema `$id` values and core evidence semantics are projected into a checked descriptor and bound to a canonical SHA-256 fingerprint. CI fails if that stable candidate changes without an explicit compatibility decision.

The candidate fingerprint is:

`sha256:cdeb7d19ad53914279b8741c0f97ec486119f1a483458dd9f9ba1549ecc25094`

## Stable contract boundary

The candidate includes:

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
- Python 3.11–3.13, Terraform and CodeQL validation.

## Quickstart

```bash
python -m pip install -e .
python scripts/verify_stable_contract.py
```

Validate a public contract:

```bash
saassecops validate examples/reference-architecture.json --kind posture
```

Inspect the package contract snapshot:

```bash
saassecops contract-snapshot
```

Verify the exact bytes of a file:

```bash
saassecops digest contracts/v1-candidate.json
```

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

The remaining path is intentionally narrow: v0.9 performs the v1 release-candidate review against one exact SHA; v1.0 promotes the already verified stable contract rather than introducing a new feature set. See [ROADMAP.md](ROADMAP.md).

## Explicit non-claims

SaaSSecOps does **not** establish deployed security effectiveness, production key custody, vulnerability absence, penetration-test success, certification, regulatory compliance, contractual acceptance or customer approval. Cryptographic verification and a stable contract fingerprint prove repository integrity/compatibility properties only; they do not prove the truth or operational effectiveness of underlying security claims.

## Author

Bilge Kayalı

## License

Apache License 2.0.
