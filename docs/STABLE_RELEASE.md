# v1.0 Stable Release

## Summary

SaaSSecOps v1.0.0 promotes the release-candidate contract verified in v0.9.0 to the stable public boundary. The promotion intentionally does not introduce a new CLI shape, public schema identity or evidence semantic.

Stable-contract fingerprint:

`sha256:d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

## Promotion rule

The v1.0 release is accepted only when:

- package metadata reports `1.0.0`;
- the v0.9 release-candidate fingerprint, checked fingerprint and live parser/schema projection are identical;
- the required security, architecture, compatibility and release documents are present;
- the repository-owned critical/high blocker register is clear;
- Python 3.11–3.13 tests and public contract validations pass;
- tenant-isolation, customer-trust and evidence-integrity negative gates remain fail-closed;
- CycloneDX SBOM, dependency audit, clean wheel installation and CLI smoke checks pass;
- both Terraform roots validate with the pinned Terraform version;
- CodeQL succeeds on the same source SHA;
- the `v1.0.0` tag is applied to the verified `main` commit and the tagged release-evidence workflow succeeds;
- build provenance is emitted for the tagged distribution artifacts.

The machine-readable repository checklist is `release/v1-stable-checklist.json`.

## Stable public boundary

The stable v1 boundary consists of the documented `saassecops` executable and command shapes, the public JSON Schema identities listed in the checked contract, deterministic assessment identity semantics, exact-byte SHA-256 digest semantics, evidence-manifest binding semantics and fail-closed handling for unsupported contract kinds/future schema versions.

Reference Terraform, diagrams, documentation prose, release scripts and internal Python modules remain non-API examples unless explicitly promoted.

## Release evidence

PR CI produces an exact-source stable review, distribution files, CycloneDX SBOM and release manifest for the candidate SHA. The tagged workflow rebuilds from the exact tag source and emits GitHub build provenance for the distribution artifacts.

Stable status therefore describes repository compatibility, packaging and evidence-integrity properties. It is not evidence that the reference architecture has been deployed.

## Limitations

v1.0.0 does not establish production AWS control effectiveness, tenant-isolation effectiveness in a deployed SaaS, production private-key custody, vulnerability absence, penetration-test success, compliance, certification, independent assurance, contractual acceptance or customer approval.
