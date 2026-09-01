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

### v0.6.0 — Customer Trust & Security GTM

Release gate:

- evidence-bound security-questionnaire response schema;
- customer-facing architecture assurance pack;
- penetration-test/audit/security-review exception register;
- responsibility matrix across Security Engineering, Product, Legal, GRC and Security GTM;
- fail-closed rules preventing unsupported affirmative, independent-assessment or certification claims;
- CI demonstration that unresolved deployment-specific questions remain `needs_review`.

### v0.7.0 — Evidence Integrity & Automation
- signed evidence envelopes, key lifecycle/revocation, release checksums/source binding, provenance and stale-evidence decisions.

### v0.8.0 — Stable Public Contract Candidate
- frozen CLI/schema identities, SemVer policy, contract fingerprint and migration policy.

### v0.9.0 — v1 Release Candidate
- full docs/threat-model review, exact-SHA release checklist and all security/release gates green.

### v1.0.0 — Stable Security Reference
- stable public contract, exact-source release evidence and explicit stable-reference non-claims.

## v1.0 public surface target

- `saassecops validate`
- `saassecops assess`
- `saassecops digest`
- `saassecops contract-snapshot`
- versioned JSON Schemas
- deterministic assessment/evidence identity rules
- reference Terraform and architecture documentation as non-API examples
