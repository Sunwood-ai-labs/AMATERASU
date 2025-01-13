# メインのネットワーキングモジュール

module "core" {
  source = "./core"
  
  project_name      = var.project_name
  aws_region        = var.aws_region
  vpc_id            = var.vpc_id
  vpc_cidr          = var.vpc_cidr
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  security_group_id = var.security_group_id
  domain           = var.domain
  subdomain        = var.subdomain
  domain_internal  = var.domain_internal
  instance_id            = var.instance_id
  alb_domain_name        = var.alb_domain_name
  alb_alt_names          = var.alb_alt_names
  instance_private_ip = var.instance_private_ip
  instance_private_dns = var.instance_private_dns
  route53_zone_id  = var.route53_zone_id
  enable_health_check = false
}
