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

# データソース定義
data "aws_route53_zone" "private" {
  zone_id = var.route53_zone_id
  private_zone = true
}

