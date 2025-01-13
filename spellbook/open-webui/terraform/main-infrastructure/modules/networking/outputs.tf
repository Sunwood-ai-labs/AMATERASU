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

output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = module.core.ec2_security_group_id
}

output "dns_record_info" {
  description = "プライベートホストゾーンのDNSレコード情報"
  value       = module.core.dns_record_info
}

output "alb_info" {
  description = "Application Load Balancer情報"
  value       = module.core.alb_info
}

output "target_group_info" {
  description = "ターゲットグループ情報"
  value       = module.core.target_group_info
}
