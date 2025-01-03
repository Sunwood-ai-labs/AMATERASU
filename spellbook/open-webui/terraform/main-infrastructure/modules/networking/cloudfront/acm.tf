# CloudFront用のACM証明書（us-east-1リージョンに作成）
resource "aws_acm_certificate" "cloudfront" {
  provider          = aws.us_east_1
  domain_name       = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"

  tags = {
    Name = "${var.project_name}-cloudfront-cert"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Route53ゾーンのデータソース
data "aws_route53_zone" "selected" {
  name         = var.domain
  private_zone = false
}

# DNS検証用のレコードを作成
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.selected.zone_id
}

# 証明書の検証完了を待機
resource "aws_acm_certificate_validation" "cloudfront" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
