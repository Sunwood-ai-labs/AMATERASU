# Route53ゾーンの取得
data "aws_route53_zone" "main" {
  provider = var.providers.aws
  name = var.domain
  private_zone = false
}

# CloudFrontのエイリアスレコードを作成
resource "aws_route53_record" "cloudfront_alias" {
  provider = var.providers.aws
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}
