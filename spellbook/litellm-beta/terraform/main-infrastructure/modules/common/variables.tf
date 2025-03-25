# Common variables used across multiple modules

variable "project_name" {
  description = "Name of the project (used as a prefix for all resources)"
  type        = string
}

variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "ap-northeast-1"
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
  description = "Base domain name for the application"
  type        = string
  default     = "sunwood-ai-labs.click"
}

variable "subdomain" {
  description = "Subdomain prefix for the application"
  type        = string
  default     = "amaterasu-open-web-ui-dev"
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

# Common locals
locals {
  name_prefix = "${var.project_name}-"
  fqdn        = "${var.subdomain}.${var.domain}"
}
