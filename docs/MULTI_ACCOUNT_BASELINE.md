# Multi-Account Security Baseline

## Summary

The v0.3 reference separates organization governance, security operations, durable audit storage and SaaS workloads into distinct AWS account boundaries.

```text
AWS Organizations management account
|
+-- Security OU
|   +-- security-tooling
|   |   +-- CloudTrail delegated administration
|   |   +-- GuardDuty delegated administration
|   |   +-- Security Hub CSPM delegated administration
|   |
|   +-- log-archive
|       +-- organization CloudTrail destination
|       +-- security/audit log retention boundary
|
+-- Workloads OU
    +-- workload-prod
    +-- workload-nonprod
```

The management account is reserved for organization-level tasks and is not a workload account. The security-tooling account is the operational security administration boundary. The log-archive account is a separate custody boundary for centralized audit evidence.

## Account responsibilities

| Account | Reference responsibility |
| --- | --- |
| management | Organizations governance, policy attachment and actions that require the management account |
| security-tooling | Delegated security administration, findings aggregation, response coordination and security-read access |
| log-archive | Central audit/security log storage with tightly restricted modification paths |
| workload-prod | Production SaaS workload resources and workload-specific controls |
| workload-nonprod | Development/test SaaS workload resources without production dependencies |

## Organization logging

The reference organization trail is intended to:

- include the management account and all member accounts;
- be multi-Region;
- enable CloudTrail log-file validation;
- deliver to a bucket owned by the log-archive account;
- separate trail administration from log custody;
- retain organization-specific KMS, bucket-policy, Object Lock and lifecycle decisions as deployment-owner responsibilities.

CloudTrail delivery and bucket access must be verified after deployment. A configured trail is not evidence that every required event has been retained or consumed by detection workflows.

## Guardrails

The repository includes two illustrative SCPs:

- `deny-leave-organization.json` blocks member-account self-removal from the organization;
- `protect-security-services.json` protects selected CloudTrail, GuardDuty, Security Hub CSPM and AWS Config control-plane actions except for explicitly named security administration or break-glass roles.

The role names are reference placeholders. A deploying organization must replace them with its own identity design and test every SCP in a policy-staging or non-production OU before broad attachment.

SCPs define maximum permissions; they do not grant IAM permissions and do not by themselves establish secure configuration.

## Delegated administration

See [Delegated Administration](DELEGATED_ADMINISTRATION.md) for service-specific boundaries. Security Hub CSPM and GuardDuty administration is Region-sensitive. CloudTrail organization administration can be delegated to a member account, while the organization trail destination remains in the separate log-archive account.

## Evidence expected from a real deployment

A production assurance package would normally retain:

- organization ID and OU/account inventory;
- attached SCP IDs, policy digests and effective-policy evidence;
- delegated-administrator account IDs by service and Region;
- organization-trail configuration and current logging status;
- log-archive bucket policy, KMS policy, retention/versioning/Object Lock configuration where applicable;
- GuardDuty organization configuration;
- Security Hub CSPM central configuration and enabled standards/controls;
- test evidence showing denied security-service disable/delete attempts from unauthorized roles;
- incident-response access paths to centralized findings and logs.

None of this deployment evidence is claimed by the repository itself.

## AWS references

- AWS Organizations OU best practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous_best_practices.html
- AWS Organizations management-account best practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html
- AWS Security Reference Architecture — Log Archive: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/log-archive.html
- AWS Security Reference Architecture — Security Tooling: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/security-tooling.html
