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
  description = "The FQDN of the created Route53 record"
  value       = module.core.route53_record_fqdn
}

# 証明書の出力
output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.core.certificate_arn
}
