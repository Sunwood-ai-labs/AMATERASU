# メインのネットワーキング設定

# データソースモジュール
module "data_sources" {
  source = "../data-sources"

  vpc_id            = var.vpc_id
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  domain            = var.domain
}

# ACMモジュール
module "acm" {
  source = "../acm"

  project_name    = var.project_name
  domain          = var.domain
  subdomain       = var.subdomain
  route53_zone_id = module.data_sources.route53_zone_id
}

# ALBモジュール
module "alb" {
  source = "../alb"

  project_name           = var.project_name
  vpc_id                = module.data_sources.vpc_id
  public_subnet_id      = module.data_sources.public_subnet_id
  public_subnet_2_id    = module.data_sources.public_subnet_2_id
  alb_security_group_id = var.security_group_id
  certificate_arn       = module.acm.certificate_arn
}

# Route53モジュール
module "route53" {
  source = "../route53"

  project_name     = var.project_name
  domain          = var.domain
  subdomain       = var.subdomain
  route53_zone_id = module.data_sources.route53_zone_id
  alb_dns_name    = module.alb.alb_dns_name
  alb_zone_id     = module.alb.alb_zone_id
  alb_depends_on  = [module.alb]

  enable_health_check = var.enable_health_check
}
