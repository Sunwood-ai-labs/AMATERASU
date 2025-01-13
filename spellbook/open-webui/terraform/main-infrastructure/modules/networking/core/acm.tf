# プライベートCA
resource "aws_acmpca_certificate_authority" "ca" {
  type = "ROOT"
  certificate_authority_configuration {
    key_algorithm     = "RSA_2048"
    signing_algorithm = "SHA256WITHRSA"
    subject {
      common_name = var.domain_internal
    }
  }

  tags = {
    Name = "${var.project_name}-private-ca"
  }
}

# ALB用の証明書（プライベートCAを使用）
resource "aws_acm_certificate" "alb" {
  domain_name               = var.alb_domain_name
  validation_method         = "DNS"
  subject_alternative_names = var.alb_alt_names
  options {
    certificate_transparency_logging_preference = "ENABLED"
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.project_name}-alb"
  }
}

