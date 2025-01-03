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

# CloudFrontモジュール
module "cloudfront" {
  source = "./cloudfront"

  project_name     = var.project_name
  domain          = var.domain
  subdomain       = var.subdomain
  alb_dns_name    = module.core.alb_dns_name
  alb_zone_id     = module.core.alb_zone_id
  route53_zone_id = module.core.route53_zone_id
  
  # 既存のRoute53レコードの情報を渡す
  existing_record_id     = module.core.route53_internal_record_id
  wait_for_existing_record = true

  providers = {
    aws.us_east_1 = aws.us_east_1
  }

  depends_on = [
    module.core,
    module.core.route53_internal_record_id
  ]
}
