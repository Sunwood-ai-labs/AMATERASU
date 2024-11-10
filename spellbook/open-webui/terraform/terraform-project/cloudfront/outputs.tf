output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.id
}

output "cloudfront_arn" {
  description = "ARN of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.arn
}

output "cloudfront_status" {
  description = "Current status of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.status
}

output "cloudfront_aliases" {
  description = "Extra CNAMEs of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.aliases
}

output "cloudfront_origin_access_identity" {
  description = "CloudFront origin access identity"
  value       = aws_cloudfront_distribution.main.origin[0].domain_name
}
