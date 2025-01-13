module "vpc" {
  source = "./modules/vpc"
  
  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
  
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  
  aws_region = var.aws_region
  tags       = var.tags
}

module "security" {
  source = "./modules/security"
  
  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  whitelist_entries = local.whitelist_entries
  tags              = var.tags
}

module "route53" {
  source = "./modules/route53"
  
  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = module.vpc.vpc_id
  domain_name     = var.domain_name
  domain_internal = var.domain_internal
  tags            = var.tags
}
