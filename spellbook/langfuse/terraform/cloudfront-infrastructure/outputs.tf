output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution (*.cloudfront.net)"
  value       = module.cloudfront.cloudfront_domain_name
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = module.cloudfront.cloudfront_distribution_id
}

output "cloudfront_arn" {
  description = "ARN of the CloudFront distribution"
  value       = module.cloudfront.cloudfront_arn
}

output "cloudfront_url" {
  description = "CloudFrontのURL"
  value       = module.cloudfront.cloudfront_url
}

output "subdomain_url" {
  description = "サブドメインのURL"
  value       = module.cloudfront.subdomain_url
}

output "waf_web_acl_id" {
  description = "ID of the WAF Web ACL"
  value       = module.cloudfront.waf_web_acl_id
}

output "waf_web_acl_arn" {
  description = "ARN of the WAF Web ACL"
  value       = module.cloudfront.waf_web_acl_arn
}

output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.cloudfront.certificate_arn
}
