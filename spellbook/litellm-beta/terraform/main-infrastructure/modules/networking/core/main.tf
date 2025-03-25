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

# プライベートホストゾーンの参照
data "aws_route53_zone" "private" {
  zone_id = var.route53_internal_zone_id  # プライベートゾーンIDを正しく指定
  private_zone = true
}

# パブリックホストゾーンの参照
data "aws_route53_zone" "public" {
  zone_id = var.route53_zone_id  # パブリックゾーンIDを指定
  private_zone = false
}
