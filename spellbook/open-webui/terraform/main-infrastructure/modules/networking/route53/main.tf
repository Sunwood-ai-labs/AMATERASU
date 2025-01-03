# パブリックホストゾーンのデータソース
data "aws_route53_zone" "public" {
  name         = var.domain
  private_zone = false
}

# パブリックDNSレコード
resource "aws_route53_record" "public" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }

  depends_on = [var.alb_depends_on]
}

# プライベートホストゾーン（オプション）
resource "aws_route53_zone" "private" {
  count = var.create_private_zone ? 1 : 0
  
  name = var.domain
  
  vpc {
    vpc_id = var.vpc_id
  }

  tags = {
    Name = "${var.project_name}-private-zone"
  }
}

# プライベートDNSレコード（オプション）
resource "aws_route53_record" "private" {
  count = var.create_private_zone ? 1 : 0
  
  zone_id = aws_route53_zone.private[0].id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}

# ヘルスチェック（オプション）
resource "aws_route53_health_check" "alb" {
  count = var.enable_health_check ? 1 : 0

  fqdn              = var.alb_dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    Name = "${var.project_name}-health-check"
  }
}
