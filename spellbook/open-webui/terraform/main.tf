terraform {
  required_version = ">= 0.12"
}

module "networking" {
  source = "./modules/networking"
  
  vpc_cidr           = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  project_name       = var.project_name
  aws_region         = var.aws_region

  providers = {
    aws           = aws
    aws.us-east-1 = aws.us-east-1
  }
}

module "compute" {
  source = "./modules/compute"
  
  project_name         = var.project_name
  vpc_id               = module.networking.vpc_id
  public_subnet_id     = module.networking.public_subnet_id
  ami_id               = var.ami_id
  instance_type        = var.instance_type
  key_name             = var.key_name
  iam_instance_profile = module.iam.ec2_instance_profile_name
  security_group_id    = module.networking.security_group_id
}

module "iam" {
  source = "./modules/iam"
  
  project_name = var.project_name
}
