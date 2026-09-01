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
- evidence-bound questionnaire, architecture assurance pack, exception register, responsibility matrix and fail-closed customer-answer rules.

### v0.7.0 — Evidence Integrity & Automation

Release gate:

- Ed25519 signed evidence-envelope contract;
- signing-key lifecycle registry with explicit active/retired/revoked states;
- fail-closed verification for tampering and revoked keys;
- freshness decisions for `current`, `revalidation_due` and `expired` evidence;
- exact Git source-SHA binding in evidence and release manifests;
- exact-byte SHA-256 checksums for built distributions and CycloneDX SBOM;
- release-evidence CI artifact bundle;
- tag-triggered GitHub build-provenance attestation workflow;
- no committed production private signing key.

### v0.8.0 — Stable Public Contract Candidate

Release gate:

- freeze the four-command public CLI surface;
- freeze v1 candidate JSON Schema identities;
- explicit SemVer compatibility policy for schemas and generated evidence;
- checked-in contract snapshot and deterministic fingerprint;
- CI gate detecting unreviewed public-contract drift;
- v0.x to v1 migration policy;
- complete public non-claim inventory.

### v0.9.0 — v1 Release Candidate

Release gate:

- full documentation and architecture review;
- threat-model review across cloud, tenant isolation, AppSec, trust and evidence integrity;
- clean package install and CLI smoke tests on the exact candidate SHA;
- Terraform, CodeQL, dependency, SBOM and release-evidence gates green on one exact commit;
- no unresolved repository-owned critical/high defects;
- v1 release checklist completed against the exact candidate SHA.

### v1.0.0 — Stable Security Reference

Release gate:

- all v0.2–v0.9 control boundaries retained;
- version, schemas, CLI and documentation aligned at `1.0.0`;
- stable-contract fingerprint verified;
- release artifacts and provenance bound to the exact tagged source revision;
- all mandatory CI/release gates green on the tagged commit;
- explicit statement that stable reference status is not a deployment, certification, compliance or independent-assessment claim.

## v1.0 public surface target

- `saassecops validate`
- `saassecops assess`
- `saassecops digest`
- `saassecops contract-snapshot`
- versioned JSON Schemas
- deterministic assessment/evidence identity rules
- reference Terraform and architecture documentation as non-API examples
