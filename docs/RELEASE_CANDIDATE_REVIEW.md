# v1 Release Candidate Review

## Summary

v0.9.0 is the release-candidate review layer for SaaSSecOps. It does not add a new public security contract. The v1 candidate fingerprint remains:

`sha256:d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

The objective is to show that the already frozen public surface can be built, installed, exercised and reviewed from one exact source revision.

## Candidate gates

The machine-readable checklist is `release/v1-rc-checklist.json`. CI requires the following on the same candidate revision:

- Python 3.11, 3.12 and 3.13 repository tests;
- stable-contract fingerprint verification;
- public JSON Schema validation;
- tenant-isolation negative vectors;
- customer-trust fail-closed checks;
- evidence signature, payload binding, freshness and revocation checks;
- CycloneDX 1.7 SBOM generation and verification;
- strict dependency vulnerability audit;
- reference and intentionally risky assessment paths;
- package build;
- wheel installation into an isolated virtual environment;
- CLI smoke tests executed outside the source tree;
- exact-source release manifest;
- both Terraform reference roots validated with Terraform 1.16.0;
- release-candidate review artifact generation;
- CodeQL on the same commit SHA.

## Clean-install boundary

The release-candidate job builds the wheel from the candidate checkout, creates a fresh virtual environment under `/tmp`, installs the wheel rather than the editable source tree, changes the working directory outside the checkout, and then exercises `saassecops --version`, `contract-snapshot`, `validate` and `digest`.

This detects packaging errors that editable installs can hide.

## Documentation review

The release gate requires the architecture, multi-account, tenant-isolation, application/API, customer-trust, evidence-integrity, compatibility, migration and threat-model documents to exist. The threat model is reviewed across cloud/organization, tenant isolation, AppSec/API, software supply chain, customer trust, evidence integrity and incident-response/operations domains.

## Defect policy

`release/defect-register.json` is the repository-owned blocker register. Any `open` or `accepted_for_fix` entry with `critical` or `high` severity blocks the release-candidate review.

The register does not claim that undiscovered defects do not exist.

## External gate

CodeQL is intentionally a separate GitHub workflow. v0.9 is merge-ready only when CodeQL and the main CI workflow both succeed on the same PR head SHA. The generated repository review artifact records CodeQL as an external same-SHA gate rather than pretending to observe a result it cannot verify from inside the Python process.

## Limitations

Release-candidate status is a repository quality and compatibility statement. It is not evidence of a deployed AWS environment, operational tenant isolation, production key custody, penetration-test success, certification, compliance or customer acceptance.
