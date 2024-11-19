# Common outputs used across multiple modules

output "project_name" {
  description = "Name of the project"
  value       = var.project_name
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = var.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = var.vpc_cidr
}

output "public_subnet_id" {
  description = "ID of the first public subnet"
  value       = var.public_subnet_id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = var.public_subnet_2_id
}

output "domain" {
  description = "Base domain name"
  value       = var.domain
}

output "subdomain" {
  description = "Subdomain prefix"
  value       = var.subdomain
}

output "tags" {
  description = "Common tags for all resources"
  value       = var.tags
}

output "name_prefix" {
  description = "Common prefix for resource names"
  value       = local.name_prefix
}

output "fqdn" {
  description = "Fully qualified domain name"
  value       = local.fqdn
}
