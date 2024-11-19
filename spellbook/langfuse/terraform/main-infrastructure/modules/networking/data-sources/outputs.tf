output "vpc_id" {
  description = "ID of the VPC"
  value       = data.aws_vpc.existing.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = data.aws_vpc.existing.cidr_block
}

output "public_subnet_id" {
  description = "ID of the first public subnet"
  value       = data.aws_subnet.public_1.id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = data.aws_subnet.public_2.id
}

output "route53_zone_id" {
  description = "ID of the Route53 hosted zone"
  value       = data.aws_route53_zone.main.zone_id
}

output "domain_name" {
  description = "Domain name from Route53 zone"
  value       = data.aws_route53_zone.main.name
}
