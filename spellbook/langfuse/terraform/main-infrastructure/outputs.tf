output "instance_id" {
  description = "ID of the EC2 instance"
  value       = module.compute.instance_id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.compute.instance_public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = module.compute.instance_private_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = module.compute.instance_public_dns
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = module.networking.public_subnet_id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.networking.alb_dns_name
}

output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = module.networking.alb_target_group_arn
}

output "application_url" {
  description = "URL of the application"
  value       = "https://${var.subdomain}.${var.domain}"
}

output "application_url_http" {
  description = "HTTP URL of the application (redirects to HTTPS)"
  value       = "http://${var.subdomain}.${var.domain}"
}
