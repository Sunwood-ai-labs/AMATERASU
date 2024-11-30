# Route53レコードの設定

# ALBのエイリアスレコード
resource "aws_route53_record" "alb" {
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

# ヘルスチェック用のレコード（必要な場合）
resource "aws_route53_health_check" "alb" {
  count             = var.enable_health_check ? 1 : 0
  fqdn              = var.alb_dns_name
  port              = 443
  type             = "HTTPS"
  resource_path    = "/"
  failure_threshold = "3"
  request_interval = "30"

  tags = {
    Name = "${var.project_name}-health-check"
  }
}


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

# プライベートホストゾーンにALBのレコードを追加
resource "aws_route53_record" "private_alb" {
  zone_id = aws_route53_zone.private.zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
