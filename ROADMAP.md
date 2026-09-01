# SaaSSecOps v1.0 Roadmap

## Summary

SaaSSecOps reaches v1.0 when it exposes a stable, documented and machine-verifiable AWS SaaS security reference contract. Version numbers represent completed repository/control boundaries; they do not imply deployment, certification or independent assessment.

## Milestones

### v0.2.0 — Contract & Evidence Foundation ✅
- strict JSON Schema contracts, deterministic evidence identity, Python 3.11–3.13 CI and Terraform validation.

### v0.3.0 — AWS Multi-Account Security Baseline ✅
- Security Tooling / Log Archive / workload separation, Organizations/SCP references and delegated security administration.

### v0.4.0 — Tenant Isolation Patterns ✅
- pool/silo/bridge patterns, authoritative tenant context, STS/session-tag reference and cross-tenant negative tests.

### v0.5.0 — Application & API Security ✅
- OWASP 2025/2023 mappings, secure-SDLC evidence, CodeQL, dependency audit, CycloneDX 1.7 and vulnerability evidence.

### v0.6.0 — Customer Trust & Security GTM ✅
- evidence-bound questionnaire, architecture assurance pack, exception register, responsibility matrix and fail-closed customer-answer rules.

### v0.7.0 — Evidence Integrity & Automation ✅
- Ed25519 evidence envelopes, key lifecycle/revocation, freshness decisions, exact-source release manifest, SBOM/release evidence bundle and tagged build provenance.

### v0.8.0 — Stable Public Contract Candidate ✅
- actual CLI/parser projection, frozen schema identities, SemVer candidate policy, migration guidance and SHA-256 contract fingerprint.

### v0.9.0 — v1 Release Candidate ✅
- expanded threat-model review, isolated wheel install, exact-head-SHA evidence binding, blocker register, pinned Actions, CodeQL v4 and Terraform 1.16.0 validation.

### v1.0.0 — Stable Security Reference ✅

Stable promotion gate:

- all v0.2–v0.9 control boundaries retained;
- package version and documentation aligned at `1.0.0`;
- v0.9 RC fingerprint retained unchanged;
- stable-release checklist and exact-SHA repository review pass;
- Python 3.11–3.13, public contract, tenant-isolation, customer-trust, evidence-integrity, SBOM, dependency and packaging gates green;
- clean wheel install and CLI smoke outside the source checkout;
- both Terraform roots validate with Terraform 1.16.0;
- CodeQL green on the same source SHA;
- no known repository-owned open critical/high release blockers;
- `v1.0.0` tag applied to the verified `main` commit;
- tagged release-evidence workflow rebuilds from the exact tag source and emits build provenance.

## v1.0 stable public surface

- `saassecops validate`
- `saassecops assess`
- `saassecops digest`
- `saassecops contract-snapshot`
- checked public JSON Schema identities
- deterministic assessment/evidence identity rules
- exact-byte SHA-256 and evidence-binding semantics
- reference Terraform and architecture documentation as non-API examples

## Post-v1 policy

v1.x may add backward-compatible functionality while preserving the checked stable boundary. Incompatible CLI/schema/semantic changes require a future major release unless a versioned parallel contract is introduced. Security fixes may tighten validation when necessary to prevent unsafe acceptance, with migration guidance where the behavior affects existing consumers.
