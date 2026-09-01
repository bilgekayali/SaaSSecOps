# Organization Guardrail Reference

## Scope

This directory contains an opt-in Terraform reference for two AWS Organizations SCPs. It does not create an AWS Organization, OUs, member accounts, delegated administrators or an organization trail.

`manage_organization_guardrails` defaults to `false`. This is intentional: organization-level SCP changes can have broad impact and should not be applied from a portfolio/reference repository without deployment-specific review.

## Validation

```bash
terraform init -backend=false
terraform validate
```

A deployment owner can inspect a plan without enabling resources:

```bash
terraform plan
```

After replacing the reference security-admin/break-glass role patterns and testing the policies in a safe OU, an authorized organization administrator can explicitly opt in:

```bash
terraform plan \
  -var='manage_organization_guardrails=true' \
  -var='guardrail_target_ids=["ou-xxxx-yyyyyyyy"]'
```

Do not apply these examples directly to an organization root before policy-staging tests, break-glass validation and impact review.
