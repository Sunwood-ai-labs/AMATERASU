terraform {
  required_version = ">= 0.12"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# CloudFront用のACM証明書はus-east-1リージョンに作成する必要があります
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

# SSMパラメータストアから必要な情報を取得
data "aws_ssm_parameter" "alb_dns_name" {
  name = "/${var.project_name}/alb_dns_name"
}

data "aws_ssm_parameter" "certificate_arn" {
  name = "/${var.project_name}/certificate_arn"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "main" {
  enabled = true
  
  origin {
    domain_name = data.aws_ssm_parameter.alb_dns_name.value
    origin_id   = "${var.project_name}-alb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${var.project_name}-alb"

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_ssm_parameter.certificate_arn.value
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}
