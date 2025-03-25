# プライベートホストゾーンの参照
data "aws_route53_zone" "private" {
  zone_id = var.route53_internal_zone_id
  private_zone = true
}

# パブリックホストゾーンの参照
data "aws_route53_zone" "public" {
  zone_id = var.route53_zone_id
  private_zone = false
}

# 内部用DNSレコード
resource "aws_route53_record" "internal" {
  zone_id = data.aws_route53_zone.private.id
  name    = "${var.subdomain}.${var.domain_internal}"
  type    = "A"

  alias {
    name                   = aws_lb.internal.dns_name
    zone_id                = aws_lb.internal.zone_id
    evaluate_target_health = true
  }

  depends_on = [
    aws_lb.internal
  ]
}

# パブリックDNSレコード
resource "aws_route53_record" "public" {
  zone_id = data.aws_route53_zone.public.id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_lb.public.dns_name
    zone_id                = aws_lb.public.zone_id
    evaluate_target_health = true
  }

  depends_on = [
    aws_lb.public,
    aws_acm_certificate_validation.public
  ]
}

# ヘルスチェック（オプション）
resource "aws_route53_health_check" "public" {
  count             = var.enable_health_check ? 1 : 0
  fqdn              = "${var.subdomain}.${var.domain}"
  port              = 443
  type             = "HTTPS"
  resource_path    = "/"
  failure_threshold = "3"
  request_interval = "30"

  depends_on = [
    aws_route53_record.public,
    aws_acm_certificate_validation.public
  ]

  tags = {
    Name = "${var.project_name}-health-check"
  }
}

resource "aws_route53_health_check" "internal" {
  count             = var.enable_health_check ? 1 : 0
  fqdn              = "${var.subdomain}.${var.domain_internal}"
  port              = 443
  type             = "HTTPS"
  resource_path    = "/"
  failure_threshold = "3"
  request_interval = "30"

  depends_on = [aws_route53_record.internal]

  tags = {
    Name = "${var.project_name}-internal-health-check"
  }
}
