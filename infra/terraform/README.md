# Terraform reference baseline

This directory demonstrates an **account-scoped** security baseline. It is not a complete SaaS deployment.

## Creates

- customer-managed KMS key for reference audit evidence;
- private, versioned and encrypted S3 audit archive;
- multi-Region CloudTrail with log-file validation;
- GuardDuty detector;
- Security Hub account enablement;
- account-level IAM Access Analyzer.

## Usage

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan \
  -var='audit_bucket_name=replace-with-a-globally-unique-name'
```

Applying this configuration can create billable AWS resources. Review the plan and AWS service costs before use.

A production implementation should add organization-level controls, delegated security administration, centralized security/logging accounts, environment separation, workload-specific tenant-isolation controls, retention/lifecycle policy, alert routing and tested incident-response automation.
