variable "region" {
  description = "AWS Region used by the management-account provider for reference policy administration."
  type        = string
  default     = "eu-west-2"
}

variable "manage_organization_guardrails" {
  description = "Explicit opt-in. When true, create and attach the reference SCPs. Keep false until organization-specific review is complete."
  type        = bool
  default     = false
}

variable "guardrail_target_ids" {
  description = "Organization root, OU or account IDs to receive both reference SCPs after explicit opt-in."
  type        = set(string)
  default     = []
}
