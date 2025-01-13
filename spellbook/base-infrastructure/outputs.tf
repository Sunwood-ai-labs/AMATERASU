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

output "whitelist_security_group_id" {
  description = "ID of the whitelist security group"
  value       = module.security.whitelist_security_group_id
}

output "cloudfront_security_group_id" {
  description = "ID of the CloudFront security group"
  value       = module.security.cloudfront_security_group_id
}

output "vpc_internal_security_group_id" {
  description = "ID of the VPC internal security group"
  value       = module.security.vpc_internal_security_group_id
}

output "route53_zone_id" {
  description = "ID of the Route53 private hosted zone"
  value       = module.route53.zone_id
}

output "route53_zone_name" {
  description = "Name of the Route53 private hosted zone"
  value       = module.route53.zone_name
}

output "route53_internal_zone_id" {
  description = "ID of the internal Route53 private hosted zone"
  value       = module.route53.internal_zone_id
}

output "route53_internal_zone_name" {
  description = "Name of the internal Route53 private hosted zone"
  value       = module.route53.internal_zone_name
}
