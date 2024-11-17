# outputs.tf

output "vpc_id" {
  description = "ID of the created VPC"
  value       = module.vpc.vpc_id
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
