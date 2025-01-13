terraform {
  required_version = ">= 0.12"
}

# デフォルトプロバイダー設定
provider "aws" {
  region = var.aws_region
}

# CloudFront用のACM証明書のためのus-east-1プロバイダー
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

# IAM module
module "iam" {
  source = "./modules/iam"
  
  project_name = var.project_name
}

# Compute module
module "compute" {
  source = "./modules/compute"
  
  project_name         = var.project_name
  vpc_id              = var.vpc_id
  vpc_cidr            = var.vpc_cidr
  public_subnet_id    = var.public_subnet_id
  ami_id              = var.ami_id
  instance_type       = var.instance_type
  key_name            = var.key_name
  iam_instance_profile = module.iam.ec2_instance_profile_name
  security_group_id    = var.security_group_id
  env_file_path       = var.env_file_path
  setup_script_path   = var.setup_script_path

  depends_on = [
    module.iam
  ]
}

# Networking module
module "networking" {
  source = "./modules/networking"
  
  project_name       = var.project_name
  aws_region        = var.aws_region
  vpc_id            = var.vpc_id
  vpc_cidr          = var.vpc_cidr
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  security_group_id = var.security_group_id
  domain           = var.domain
  subdomain        = var.subdomain
  domain_internal  = var.domain_internal
  route53_zone_id  = var.route53_internal_zone_id
  instance_id      = module.compute.instance_id
  instance_private_ip = module.compute.instance_private_ip
  instance_private_dns = module.compute.instance_private_dns
  instance_public_ip = module.compute.instance_public_ip

  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }

  depends_on = [
    module.compute
  ]
}
