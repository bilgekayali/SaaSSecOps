# Changelog

## 0.4.0

- Added machine-readable pool, silo and bridge tenant-isolation patterns.
- Added authoritative tenant-context and fail-closed authorization contracts.
- Added an internal deterministic isolation decision engine for synthetic negative tests.
- Added same-tenant allow and cross-tenant/missing-context/unauthorized-action denial vectors.
- Added an AWS STS/ABAC pooled S3 prefix policy example using `aws:PrincipalTag/tenant-id`.
- Added tenant-isolation threat analysis and deployment-evidence checklist.
- Expanded the public contract snapshot with the `tenant-isolation` schema.
- Added tenant-isolation vector execution to CI.

## 0.3.0

- Added a machine-readable AWS multi-account reference contract and schema.
- Added Security OU, Security Tooling, Log Archive and workload-account separation.
- Added CloudTrail, GuardDuty and Security Hub CSPM delegated-administration guidance.
- Added organization-trail and centralized log-custody reference model.
- Added illustrative SCPs for organization membership and core security-service protection.
- Added explicit opt-in Terraform for SCP creation/attachment and CI validation.
- Expanded the public contract snapshot with the `multi-account` schema.

## 0.2.0

- Added strict posture, policy, assessment-report and evidence-manifest contracts.
- Added deterministic assessment identity and exact SHA-256 evidence bindings.
- Added `validate`, `digest` and `contract-snapshot` CLI commands.
- Added evidence-manifest generation to `assess`.
- Expanded CI to Python 3.11–3.13, package build and Terraform validation.
- Added v1 roadmap and compatibility policy.
- Added repository contract test preventing `Why ...` Markdown headings.

## 0.1.0

- Initial AWS SaaS security and trust reference architecture.
- Added tenant isolation, IAM, network, data-protection, logging, detection, incident-response and customer-trust controls.
- Added account-scoped Terraform baseline and deterministic local assessment demo.
