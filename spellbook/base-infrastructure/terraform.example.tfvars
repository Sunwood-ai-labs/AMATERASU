# terraform.tfvars

# AWS Region
aws_region = "ap-northeast-1"

# Project Information
project_name = "example-project"
environment  = "dev"

# Network Configuration
vpc_cidr             = "10.0.0.0/16"
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.10.0/24", "10.0.11.0/24"]

# Domain Configuration
domain_name      = "example.com"
domain_internal  = "example.internal"

# Resource Tags
tags = {
  Project     = "example-project"
  Environment = "dev"
  Terraform   = "true"
  Owner       = "infrastructure-team"
  Department  = "engineering"
  CostCenter  = "infrastructure"
}
