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
output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = module.core.ec2_security_group_id
}

# 証明書の出力
output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = module.core.certificate_arn
}
