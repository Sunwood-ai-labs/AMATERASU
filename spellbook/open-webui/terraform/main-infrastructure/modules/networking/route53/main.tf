# modules/networking/route53/main.tf

# プライベートホストゾーンの作成
resource "aws_route53_zone" "private" {
  name = var.domain

  vpc {
    vpc_id = var.vpc_id
  }

  tags = {
    Name = "${var.project_name}-private-zone"
  }
}

# プライベートホストゾーンにALBのエントリを追加
# これにより、VPC内からのDNSクエリは内部IPにルーティングされます
resource "aws_route53_record" "private" {
  zone_id = aws_route53_zone.private.id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}

# パブリックホストゾーンのレコード（既存）
resource "aws_route53_record" "public" {
  zone_id = var.route53_zone_id  # パブリックゾーンID
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
