# SaaSSecOps v1.0 Roadmap

## Summary

SaaSSecOps reaches v1.0 when it exposes a stable, documented and machine-verifiable AWS SaaS security reference contract. Version numbers represent completed control boundaries; they do not imply deployment, certification or independent assessment.

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
- evidence-bound questionnaire, assurance pack, trust-exception register, responsibility matrix and fail-closed customer-answer rules.

### v0.7.0 — Evidence Integrity & Automation ✅
- Ed25519 evidence envelopes, payload/source binding, signing-key lifecycle/revocation, evidence freshness, release checksums and build provenance workflow.

### v0.8.0 — Stable Public Contract Candidate ✅

Completed release gate:

- actual argparse command/argument surface projected into a checked public descriptor;
- public JSON Schema `$id` values frozen into the candidate descriptor;
- core assessment/digest/evidence semantics included in the stable boundary;
- canonical SHA-256 contract fingerprint checked into the repository;
- CI verifies descriptor and fingerprint on Python 3.11–3.13;
- SemVer compatibility policy updated for the candidate boundary;
- migration guidance added for consumers preparing for v1;
- release evidence bundle includes the checked candidate descriptor and fingerprint.

### v0.9.0 — v1 Release Candidate

Release gate:

- full documentation and architecture review;
- threat-model review across cloud, tenant, application, trust and evidence layers;
- clean wheel install and CLI smoke tests in an isolated environment;
- stable-contract fingerprint verified against one exact candidate SHA;
- Terraform, dependency audit, CodeQL, SBOM, signature/integrity and contract gates green on the same SHA;
- no unresolved repository-owned critical/high defects;
- v1 release checklist completed and source-bound to the candidate SHA.

### v1.0.0 — Stable Security Reference

Release gate:

- no new breaking public-contract change relative to the approved v0.9 candidate;
- package/documentation/version aligned at `1.0.0`;
- stable-contract fingerprint retained or intentionally versioned with documented migration;
- release artifacts and provenance bound to the exact tagged source revision;
- all mandatory release gates green on the tagged commit;
- explicit stable-reference non-claims retained.

## v1.0 public surface target

- `saassecops validate`
- `saassecops assess`
- `saassecops digest`
- `saassecops contract-snapshot`
- `saassecops --version`
- versioned public JSON Schemas
- deterministic assessment/evidence identity rules
- exact-byte digest and evidence binding semantics

Reference Terraform, diagrams, documentation prose, release scripts and internal Python modules remain non-API surfaces unless explicitly promoted.
