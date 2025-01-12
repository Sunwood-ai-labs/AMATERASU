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
output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = var.security_group_id
}

# ACM証明書の出力
output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.acm.certificate_arn
}

# Route53の出力
output "dns_name" {
  description = "The DNS name of the created record"
  value       = "${var.subdomain}.${var.domain}"
}
