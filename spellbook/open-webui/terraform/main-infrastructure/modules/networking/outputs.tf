# VPCとサブネットの出力
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.core.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.core.vpc_cidr
}

output "public_subnet_id" {
  description = "ID of the first public subnet"
  value       = module.core.public_subnet_id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = module.core.public_subnet_2_id
}

# セキュリティグループの出力
output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = module.core.alb_security_group_id
}

output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = module.core.ec2_security_group_id
}

# ALBの出力
output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = module.core.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the ALB"
  value       = module.core.alb_zone_id
}

output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = module.core.alb_target_group_arn
}

# Route53とDNSの出力
output "dns_name" {
  description = "The DNS name of the created record"
  value       = module.core.dns_name
}

output "route53_record_fqdn" {
  description = "The FQDN of the created internal Route53 record"
  value       = module.core.route53_internal_record_fqdn
}

# 証明書の出力
output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.core.certificate_arn
}

# CloudFrontの出力
output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = module.cloudfront.cloudfront_domain_name
}

output "cloudfront_hosted_zone_id" {
  description = "Route53 zone ID of the CloudFront distribution"
  value       = module.cloudfront.cloudfront_hosted_zone_id
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = module.cloudfront.cloudfront_distribution_id
}

output "cloudfront_certificate_arn" {
  description = "ARN of the CloudFront ACM certificate"
  value       = module.cloudfront.certificate_arn
}

output "cloudfront_url" {
  description = "Full URL for accessing the application through CloudFront"
  value       = "https://${module.cloudfront.domain_name}"
}
