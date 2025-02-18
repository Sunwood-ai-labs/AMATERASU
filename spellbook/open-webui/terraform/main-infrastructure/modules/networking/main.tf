# メインのネットワーキングモジュール

module "core" {
  source = "./core"
  
  project_name      = var.project_name
  aws_region        = var.aws_region
  vpc_id            = var.vpc_id
  vpc_cidr          = var.vpc_cidr
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  security_group_ids = var.security_group_ids
  domain           = var.domain
  subdomain        = var.subdomain
  domain_internal  = var.domain_internal
  instance_id            = var.instance_id
  instance_private_ip = var.instance_private_ip
  instance_private_dns = var.instance_private_dns
  instance_public_ip = var.instance_public_ip
  route53_zone_id  = var.route53_zone_id
  enable_health_check = false
}
