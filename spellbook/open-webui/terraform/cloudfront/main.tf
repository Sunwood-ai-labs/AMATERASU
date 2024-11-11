# main.tf
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

# CloudFront用の新しいセキュリティグループを作成
resource "aws_security_group" "cloudfront_alb" {
  name_prefix = "${var.project_name}-cloudfront-alb"
  description = "Security group for CloudFront to ALB communication"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow HTTP from anywhere (CloudFront)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS from anywhere (CloudFront)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(
    {
      Name = "${var.project_name}-cloudfront-alb"
    },
    var.tags
  )

  lifecycle {
    create_before_destroy = true
  }
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${var.project_name} distribution"
  
  origin {
    domain_name = var.alb_dns_name
    origin_id   = "${var.project_name}-alb"

    custom_origin_config {
      http_port                = 80
      https_port              = 443
      origin_protocol_policy  = "http-only"
      origin_ssl_protocols    = ["TLSv1.2"]
      origin_read_timeout     = 60
      origin_keepalive_timeout = 5
    }

    custom_header {
      name  = "X-Custom-Header"
      value = "CloudFront-Health-Check"
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${var.project_name}-alb"

    forwarded_values {
      query_string = true
      headers      = [
        "Host",
        "Origin",
        "Authorization",
        "Accept",
        "Accept-Language"
      ]
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = var.min_ttl
    default_ttl            = var.default_ttl
    max_ttl                = var.max_ttl
    compress              = true
  }

  # カスタムエラーレスポンスの設定
  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
    error_caching_min_ttl = 10
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
    error_caching_min_ttl = 10
  }

  price_class = var.price_class

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version    = "TLSv1.2_2021"
  }

  tags = merge(
    {
      Name        = "${var.project_name}-cloudfront"
      Environment = var.environment
    },
    var.tags
  )

  depends_on = [
    aws_security_group.cloudfront_alb
  ]
}

