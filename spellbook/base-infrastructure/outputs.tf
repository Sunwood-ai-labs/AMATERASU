output "vpc_id" {
  description = "ID of the created VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = var.vpc_cidr
}

output "public_subnet_cidrs" {
  description = "CIDR blocks of the public subnets"
  value       = var.public_subnet_cidrs
}

output "public_subnet_ids" {
  description = "IDs of the created public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the created private subnets"
  value       = module.vpc.private_subnet_ids
}

output "default_security_group_id" {
  description = "ID of the default security group"
  value       = module.security.default_security_group_id
}
