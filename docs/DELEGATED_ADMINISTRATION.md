# Delegated Administration

## Scope

The reference assigns CloudTrail, GuardDuty and Security Hub CSPM administration to the `security-tooling` account instead of using the AWS Organizations management account for day-to-day security operations.

The commands below are operational references. They require organization-specific account IDs, Regions, IAM permissions and change approval.

## CloudTrail

CloudTrail supports delegated administrators for organization trails.

From the management account:

```bash
aws organizations register-delegated-administrator \
  --account-id <SECURITY_TOOLING_ACCOUNT_ID> \
  --service-principal cloudtrail.amazonaws.com
```

The delegated administrator can then create or manage an organization trail, subject to CloudTrail permissions. A reference creation shape is:

```bash
aws cloudtrail create-trail \
  --name organization-security-trail \
  --s3-bucket-name <LOG_ARCHIVE_BUCKET> \
  --is-organization-trail \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --kms-key-id <AUDIT_KMS_KEY_ARN>

aws cloudtrail start-logging --name organization-security-trail
```

The destination bucket policy and KMS key policy must explicitly support organization-trail delivery and the intended security/log-custody model.

## GuardDuty

GuardDuty delegated administration is configured from the management account for each intended Region:

```bash
aws guardduty enable-organization-admin-account \
  --admin-account-id <SECURITY_TOOLING_ACCOUNT_ID> \
  --region <AWS_REGION>
```

The delegated administrator must separately configure organization member enrollment and feature settings. Delegation alone does not prove that every account or protection plan is enabled.

## Security Hub CSPM

Security Hub CSPM delegated administration is also designated from the management account:

```bash
aws securityhub enable-organization-admin-account \
  --admin-account-id <SECURITY_TOOLING_ACCOUNT_ID> \
  --region <AWS_REGION>
```

For central configuration, define a home Region and linked Regions, then manage organization configuration policies from the delegated administrator. Delegation alone does not establish enabled standards, controls or cross-Region aggregation.

## Verification

A deployment review should verify at least:

```bash
aws organizations list-delegated-administrators
aws cloudtrail describe-trails --include-shadow-trails
aws cloudtrail get-trail-status --name organization-security-trail
aws guardduty list-organization-admin-accounts --region <AWS_REGION>
aws securityhub list-organization-admin-accounts --region <AWS_REGION>
```

Command output is deployment evidence only when captured from the intended AWS organization, bound to time/account/Region and reviewed by an accountable owner.

## References

- CloudTrail delegated administrator: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-delegated-administrator.html
- Organization trail: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html
- GuardDuty organization permissions: https://docs.aws.amazon.com/guardduty/latest/ug/organizations_permissions.html
- Security Hub CSPM Organizations integration: https://docs.aws.amazon.com/securityhub/latest/userguide/designate-orgs-admin-account.html
