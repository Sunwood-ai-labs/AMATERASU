# modules/networking/route53/main.tf

# プライベートホストゾーンのデータソース
data "aws_route53_zone" "private" {
  name         = var.domain
  private_zone = true
  vpc_id       = var.vpc_id  # vpcブロックの代わりにvpc_idを使用
}

# プライベートホストゾーンにALBのエントリを追加
resource "aws_route53_record" "private" {
  zone_id = data.aws_route53_zone.private.zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }

  depends_on = [var.alb_depends_on]
}

# パブリックホストゾーンのレコード
resource "aws_route53_record" "public" {
  zone_id = var.route53_zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }

  depends_on = [var.alb_depends_on]
}
