variable "region" {
  description = "AWS Region for the account-scoped reference baseline."
  type        = string
  default     = "eu-west-2"
}

variable "audit_bucket_name" {
  description = "Globally unique S3 bucket name for reference CloudTrail logs."
  type        = string
}

variable "name_prefix" {
  description = "Prefix for reference resources."
  type        = string
  default     = "saassecops-reference"
}
