output "guardrails_enabled" {
  description = "Whether the reference SCP resources are opted in for this Terraform invocation."
  value       = var.manage_organization_guardrails
}

output "guardrail_targets" {
  description = "Targets supplied for explicit SCP attachment."
  value       = sort(tolist(var.guardrail_target_ids))
}
