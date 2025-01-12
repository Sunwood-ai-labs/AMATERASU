# メインのネットワーキング設定

# データソースモジュール
module "data_sources" {
  source = "../data-sources"

  vpc_id            = var.vpc_id
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = var.public_subnet_2_id
  domain            = var.domain
  subdomain         = var.subdomain
}

# ACMモジュール
module "acm" {
  source = "../acm"

  project_name    = var.project_name
  domain          = var.domain
  subdomain       = var.subdomain
}
