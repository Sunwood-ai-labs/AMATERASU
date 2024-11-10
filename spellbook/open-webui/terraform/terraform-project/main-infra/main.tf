terraform {
  required_version = ">= 0.12"
}

module "networking" {
  source = "./modules/networking"
  
  vpc_cidr           = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  project_name       = var.project_name
  aws_region         = var.aws_region
  domain_name        = var.domain_name
}

module "iam" {
  source = "./modules/iam"
  
  project_name = var.project_name
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

  depends_on = [
    module.networking,
    module.iam
  ]
}

# ALBターゲットグループにEC2インスタンスを登録
resource "aws_lb_target_group_attachment" "main" {
  target_group_arn = module.networking.alb_target_group_arn
  target_id        = module.compute.instance_id
  port             = 80

  depends_on = [
    module.compute
  ]
}
