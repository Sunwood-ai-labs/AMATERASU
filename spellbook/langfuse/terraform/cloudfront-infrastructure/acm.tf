# ACM証明書の作成（us-east-1リージョンに必要）
resource "aws_acm_certificate" "cloudfront_cert" {
  provider = aws.virginia
  domain_name = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# DNS検証用のレコードを作成
resource "aws_route53_record" "cert_validation" {
  provider = aws.virginia
  for_each = {
    for dvo in aws_acm_certificate.cloudfront_cert.domain_validation_options : dvo.domain_name => {
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
  zone_id         = data.aws_route53_zone.main.zone_id
}

# 証明書の検証完了を待機
resource "aws_acm_certificate_validation" "cert_validation" {
  provider = aws.virginia
  certificate_arn = aws_acm_certificate.cloudfront_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
