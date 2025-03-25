# パブリック用ACM証明書
resource "aws_acm_certificate" "public" {
  provider = aws
  domain_name       = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"

  tags = {
    Name = "${var.project_name}-public-certificate"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# 証明書検証用のDNSレコード（パブリック）
resource "aws_route53_record" "cert_validation_public" {
  for_each = {
    for dvo in aws_acm_certificate.public.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  zone_id = data.aws_route53_zone.public.id
  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
  ttl     = 60

  allow_overwrite = true
}

# 証明書の検証完了を待つ（パブリック）
resource "aws_acm_certificate_validation" "public" {
  certificate_arn         = aws_acm_certificate.public.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation_public : record.fqdn]
}

# 内部用の自己署名証明書
resource "tls_private_key" "internal" {
  algorithm = "RSA"
}

resource "tls_self_signed_cert" "internal" {
  private_key_pem = tls_private_key.internal.private_key_pem

  subject {
    common_name  = "${var.subdomain}.${var.domain_internal}"
    organization = "Internal Organization"
  }

  validity_period_hours = 8760  # 1年

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

resource "aws_acm_certificate" "internal" {
  private_key      = tls_private_key.internal.private_key_pem
  certificate_body = tls_self_signed_cert.internal.cert_pem

  tags = {
    Name = "${var.project_name}-internal-certificate"
  }

  lifecycle {
    create_before_destroy = true
  }
}
