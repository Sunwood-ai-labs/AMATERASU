output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution (*.cloudfront.net)"
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

output "cloudfront_url" {
  description = "CloudFrontのURL"
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "subdomain_url" {
  description = "サブドメインのURL"
  value       = "https://${var.subdomain}.${var.domain}"
}
