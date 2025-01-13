variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "vpc_id" {
  description = "ID of the existing VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "ID of the first public subnet"
  type        = string
}

variable "public_subnet_2_id" {
  description = "ID of the second public subnet"
  type        = string
}

variable "domain" {
  description = "Base domain name"
  type        = string
}

variable "subdomain" {
  description = "Subdomain prefix"
  type        = string
}

variable "domain_internal" {
  description = "Internal domain name for private hosted zone"
  type        = string
}

variable "enable_health_check" {
  description = "Whether to enable Route53 health check"
  type        = bool
  default     = false
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "security_group_id" {
  description = "ID of the existing security group"
  type        = string
}

variable "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  type        = string
}

variable "instance_private_dns" {
  description = "Private DNS name of the EC2 instance"
  type        = string
  default     = null
}

variable "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  type        = string
}

variable "route53_zone_id" {
  description = "Route53 private hosted zone ID"
  type        = string
}

variable "instance_id" {
  description = "ID of the EC2 instance to attach to the target group"
  type        = string
}


