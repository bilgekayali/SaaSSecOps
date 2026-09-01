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

### v0.7.0 — Evidence Integrity & Automation ✅
- Ed25519 evidence envelopes, key lifecycle/revocation, freshness decisions, exact-source release manifest, SBOM/release evidence bundle and tagged build provenance.

### v0.8.0 — Stable Public Contract Candidate ✅
- actual CLI/parser projection, frozen schema identities, SemVer candidate policy, migration guidance and SHA-256 contract fingerprint.

### v0.9.0 — v1 Release Candidate

Release gate:

- expanded threat-model review across cloud/organization, tenant isolation, AppSec/API, software supply chain, customer trust, evidence integrity and incident response;
- isolated wheel install and CLI smoke tests outside the source checkout;
- machine-readable release-candidate checklist and exact-SHA review artifact;
- repository-owned critical/high blocker register with fail-closed release policy;
- stable-contract fingerprint retained unchanged from v0.8;
- Python 3.11–3.13, Terraform 1.16.0, dependency, SBOM and release-evidence gates green on one candidate SHA;
- CodeQL green on the same candidate SHA;
- critical GitHub Actions pinned to reviewed commit SHAs.

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
