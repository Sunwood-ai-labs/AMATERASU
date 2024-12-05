# terraform.tfvars

aws_region   = "ap-northeast-1"
project_name = "amts-base-infrastructure"
environment  = "dev"

domain_name = "sunwood-ai-labs.click"

vpc_cidr             = "10.0.0.0/16"
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.10.0/24", "10.0.11.0/24"]

tags = {
  Project     = "amaterasu"
  Environment = "dev"
  Terraform   = "true"
}
