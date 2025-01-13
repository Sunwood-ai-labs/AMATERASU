# ALB用のプライベート証明書設定

# プライベートCA
resource "aws_acmpca_certificate_authority" "alb_ca" {
  type = "ROOT"  # ROOTに変更

  certificate_authority_configuration {
    key_algorithm     = "RSA_2048"
    signing_algorithm = "SHA256WITHRSA"

    subject {
      common_name = var.domain_internal
      country = "JP"
      organization = "Sunwood AI Labs"
      organizational_unit = "Internal CA"
      state = "Tokyo"
      locality = "Minato-ku"
    }
  }

  permanent_deletion_time_in_days = 7
  enabled = true

  tags = {
    Name = "${var.project_name}-private-ca"
  }
}

# プライベートCAのアクティベーション
resource "aws_acmpca_certificate" "root" {
  certificate_authority_arn   = aws_acmpca_certificate_authority.alb_ca.arn
  certificate_signing_request = aws_acmpca_certificate_authority.alb_ca.certificate_signing_request
  signing_algorithm          = "SHA256WITHRSA"

  template_arn = "arn:aws:acm-pca:::template/RootCACertificate/V1"

  validity {
    type  = "YEARS"
    value = 10
  }
}

resource "aws_acmpca_certificate_authority_certificate" "root" {
  certificate_authority_arn = aws_acmpca_certificate_authority.alb_ca.arn
  certificate              = aws_acmpca_certificate.root.certificate
  certificate_chain        = aws_acmpca_certificate.root.certificate_chain
}

# ALB用の証明書
resource "aws_acm_certificate" "alb_cert" {
  domain_name               = "${var.subdomain}.${var.domain_internal}"
  certificate_authority_arn = aws_acmpca_certificate_authority.alb_ca.arn
  
  subject_alternative_names = [
    "*.${var.domain_internal}"
  ]

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.project_name}-alb-cert"
    ManagedBy = "terraform"
  }

  depends_on = [
    aws_acmpca_certificate_authority_certificate.root
  ]
}
