# プライベートCA設定
resource "aws_acmpca_certificate_authority" "ca" {
  type = "ROOT"
  certificate_authority_configuration {
    key_algorithm     = "RSA_2048"
    signing_algorithm = "SHA256WITHRSA"
    subject {
      common_name = var.domain_internal
      organization = "Internal CA"
      organizational_unit = "Security"
      country = "JP"
      state = "Tokyo"
      locality = "Minato-ku"
    }
  }
  
  revocation_configuration {
    crl_configuration {
      enabled = true
      expiration_in_days = 7
      s3_bucket_name = "amaterasu-crl-${data.aws_caller_identity.current.account_id}"
    }
  }
  
  enabled = true
  tags = { Name = "${var.project_name}-ca" }
}

# プライベートCAの証明書
resource "aws_acmpca_certificate" "ca_cert" {
  certificate_authority_arn   = aws_acmpca_certificate_authority.ca.arn
  certificate_signing_request = aws_acmpca_certificate_authority.ca.certificate_signing_request
  signing_algorithm          = "SHA256WITHRSA"
  template_arn               = "arn:aws:acm-pca:::template/RootCACertificate/V1"
  
  validity {
    type  = "YEARS"
    value = 5  # 5年の有効期限
  }
}

# プライベートCAの証明書を関連付け
resource "aws_acmpca_certificate_authority_certificate" "ca_cert_assoc" {
  certificate_authority_arn = aws_acmpca_certificate_authority.ca.arn
  certificate              = aws_acmpca_certificate.ca_cert.certificate
  certificate_chain        = aws_acmpca_certificate.ca_cert.certificate_chain
}

# ALB用の証明書（プライベートCAで署名）
resource "aws_acm_certificate" "alb" {
  domain_name               = "${var.subdomain}.${var.domain_internal}"
  certificate_authority_arn = aws_acmpca_certificate_authority.ca.arn
  subject_alternative_names = ["*.${var.domain_internal}"]
  
  lifecycle {
    create_before_destroy = true
  }
  
  tags = { Name = "${var.project_name}-alb" }
  
  depends_on = [aws_acmpca_certificate_authority_certificate.ca_cert_assoc]
}

# データソース
data "aws_caller_identity" "current" {}
