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
  enable_health_check = false
}
