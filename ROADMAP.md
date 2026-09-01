# SaaSSecOps v1.0 Roadmap

## Summary

SaaSSecOps will reach v1.0 when the repository exposes a stable, documented and machine-verifiable AWS SaaS security reference contract. Version numbers represent completed control boundaries; they do not imply that the reference has been deployed or independently certified.

## Milestones

### v0.2.0 — Contract & Evidence Foundation ✅

Completed release gate:

- strict JSON Schema contracts for posture, policy, assessment report and evidence manifest;
- deterministic assessment identity and exact input/policy/report SHA-256 bindings;
- CLI validation, digest and contract-snapshot commands;
- Python 3.11–3.13 CI matrix;
- package-build smoke test;
- Terraform initialization and validation in CI;
- repository guard preventing `Why ...` Markdown headings;
- compatibility and changelog foundations.

### v0.3.0 — AWS Multi-Account Security Baseline

Release gate:

- reference security, logging and workload-account topology;
- AWS Organizations/SCP examples and explicit non-claims;
- centralized CloudTrail/log archive pattern;
- delegated GuardDuty and Security Hub administration pattern;
- AWS Config/security-account evidence references;
- separation between deployable sample code and organization-specific responsibilities.

### v0.4.0 — Tenant Isolation Patterns

Release gate:

- pooled, siloed and bridge tenancy reference patterns;
- tenant-context propagation contract;
- STS/session-tag or equivalent scoped-authorization examples;
- data-layer tenant-enforcement examples;
- negative tests demonstrating cross-tenant denial;
- isolation threat model and evidence checklist.

### v0.5.0 — Application & API Security

Release gate:

- OWASP Top 10 and API Security control family;
- secure-SDLC evidence model;
- API edge/WAF/TLS/secrets reference controls;
- dependency and code scanning gates;
- CycloneDX SBOM generation;
- vulnerability finding/exception evidence references.

### v0.6.0 — Customer Trust & Security GTM

Release gate:

- evidence-bound security-questionnaire response schema;
- customer-facing architecture assurance pack;
- penetration-test/audit exception register contract;
- responsibility matrix across Security Engineering, Product, Legal, GRC and GTM;
- explicit rules preventing unsupported `yes` answers or compliance claims.

### v0.7.0 — Evidence Integrity & Automation

Release gate:

- signed evidence-envelope reference;
- key lifecycle/revocation metadata;
- release checksum manifest and source binding;
- reproducible evidence-generation workflow;
- CI provenance/SBOM evidence for release artifacts;
- stale-evidence and revalidation decisions.

### v0.8.0 — Stable Public Contract Candidate

Release gate:

- frozen CLI command set;
- frozen JSON Schema identities;
- explicit SemVer compatibility policy;
- contract snapshot/fingerprint checked in CI;
- migration policy for v0.x to v1;
- complete non-claim inventory.

### v0.9.0 — v1 Release Candidate

Release gate:

- documentation and architecture review;
- threat-model review;
- Terraform validation and security-tooling gates green on one exact commit;
- clean package install and CLI smoke tests;
- no unresolved repository-owned critical/high defects;
- v1 release checklist completed against the exact candidate SHA.

### v1.0.0 — Stable Security Reference

Release gate:

- all v0.2–v0.9 control boundaries retained;
- version, schemas, CLI and documentation aligned at `1.0.0`;
- stable-contract fingerprint verified;
- release artifacts bound to the exact source revision;
- all mandatory CI/release gates green on the tagged commit;
- explicit statement that stable reference status is not a deployment, certification, compliance or independent-assessment claim.

## v1.0 public surface target

The intended stable boundary is deliberately small:

- `saassecops validate`
- `saassecops assess`
- `saassecops digest`
- `saassecops contract-snapshot`
- versioned JSON Schemas
- deterministic assessment/evidence identity rules
- reference Terraform and architecture documentation as non-API examples

Internal Python modules remain implementation details unless explicitly promoted before v1.0.
