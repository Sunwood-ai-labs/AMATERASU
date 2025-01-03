# CloudFront用のRoute53レコード
resource "aws_route53_record" "cloudfront" {
  zone_id         = var.route53_zone_id
  name            = "${var.subdomain}.${var.domain}"
  type            = "A"
  allow_overwrite = true

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }

  depends_on = [
    aws_cloudfront_distribution.main
  ]
}
