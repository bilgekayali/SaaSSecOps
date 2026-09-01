output "cloudtrail_name" {
  description = "Reference CloudTrail name."
  value       = aws_cloudtrail.security.name
}

output "audit_bucket_arn" {
  description = "Reference audit archive bucket ARN."
  value       = aws_s3_bucket.audit.arn
}

output "audit_kms_key_arn" {
  description = "Reference KMS key ARN."
  value       = aws_kms_key.audit.arn
}

output "access_analyzer_arn" {
  description = "Reference IAM Access Analyzer ARN."
  value       = aws_accessanalyzer_analyzer.account.arn
}
