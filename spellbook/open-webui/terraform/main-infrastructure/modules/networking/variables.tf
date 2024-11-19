# Common variables that will be passed to the common module
variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
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

# Module specific variables
variable "security_group_id" {
  description = "ID of the existing security group"
  type        = string
}

variable "enable_health_check" {
  description = "Whether to enable Route53 health check"
  type        = bool
  default     = false
}

# Common module reference
module "common" {
  source = "../common"

  project_name      = var.project_name
  aws_region       = var.aws_region
  vpc_id           = var.vpc_id
  vpc_cidr         = var.vpc_cidr
  public_subnet_id = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  domain           = var.domain
  subdomain        = var.subdomain
}

# Local variables using common module outputs
locals {
  name_prefix = module.common.name_prefix
  fqdn        = module.common.fqdn
  tags        = module.common.tags
}