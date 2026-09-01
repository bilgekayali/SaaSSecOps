provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = "SaaSSecOps"
      ManagedBy = "Terraform"
      Scope     = "ReferenceOnly"
      Milestone = "v0.3"
    }
  }
}

locals {
  deny_leave_organization    = file("${path.module}/../../policies/scp/deny-leave-organization.json")
  protect_security_services = file("${path.module}/../../policies/scp/protect-security-services.json")
}

resource "aws_organizations_policy" "deny_leave_organization" {
  count = var.manage_organization_guardrails ? 1 : 0

  name        = "SaaSSecOps-DenyLeaveOrganization"
  description = "Reference SCP preventing member accounts from leaving AWS Organizations."
  type        = "SERVICE_CONTROL_POLICY"
  content     = local.deny_leave_organization
}

resource "aws_organizations_policy" "protect_security_services" {
  count = var.manage_organization_guardrails ? 1 : 0

  name        = "SaaSSecOps-ProtectSecurityServices"
  description = "Reference SCP protecting selected security-service control-plane actions."
  type        = "SERVICE_CONTROL_POLICY"
  content     = local.protect_security_services
}

resource "aws_organizations_policy_attachment" "deny_leave_organization" {
  for_each = var.manage_organization_guardrails ? var.guardrail_target_ids : toset([])

  policy_id = aws_organizations_policy.deny_leave_organization[0].id
  target_id = each.value
}

resource "aws_organizations_policy_attachment" "protect_security_services" {
  for_each = var.manage_organization_guardrails ? var.guardrail_target_ids : toset([])

  policy_id = aws_organizations_policy.protect_security_services[0].id
  target_id = each.value
}
