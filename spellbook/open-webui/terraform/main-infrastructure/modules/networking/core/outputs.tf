# modules/networking/core/outputs.tf

# VPCとサブネットの出力
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.data_sources.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.data_sources.vpc_cidr
}

output "public_subnet_id" {
  description = "ID of the first public subnet"
  value       = module.data_sources.public_subnet_id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = module.data_sources.public_subnet_2_id
}

# セキュリティグループの出力
output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = var.security_group_id
}

output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = var.security_group_id
}

# ACM証明書の出力
output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.acm.certificate_arn
}

# ALBの出力
output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = module.alb.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the ALB"
  value       = module.alb.alb_zone_id
}

output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = module.alb.alb_target_group_arn
}

# Route53の出力
output "dns_name" {
  description = "The DNS name of the created record"
  value       = "${var.subdomain}.${var.domain}"
}

output "route53_record_fqdn" {
  description = "The FQDN of the created public Route53 record"
  value       = module.route53.public_record_fqdn
}

output "route53_private_record_fqdn" {
  description = "The FQDN of the created private Route53 record"
  value       = module.route53.private_record_fqdn
}

output "route53_private_zone_id" {
  description = "ID of the private hosted zone"
  value       = module.route53.private_zone_id
}

output "route53_zone_id" {
  description = "ID of the public Route53 hosted zone"
  value       = module.data_sources.route53_zone_id
}

output "route53_public_record_id" {
  description = "ID of the public Route53 A record"
  value       = module.route53.public_record_id
}
