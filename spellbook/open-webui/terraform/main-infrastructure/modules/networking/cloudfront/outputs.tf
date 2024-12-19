output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "cloudfront_hosted_zone_id" {
  description = "Route53 zone ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.hosted_zone_id
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.id
}

output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = aws_acm_certificate.cloudfront.arn
}

output "domain_name" {
  description = "Full domain name for the CloudFront distribution"
  value       = "${var.subdomain}.${var.domain}"
}
