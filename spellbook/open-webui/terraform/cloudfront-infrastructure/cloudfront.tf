# CloudFrontディストリビューション設定
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled    = true
  price_class        = "PriceClass_200"
  retain_on_delete   = false
  wait_for_deployment = false
  web_acl_id         = aws_wafv2_web_acl.cloudfront_waf.arn

  origin {
    domain_name = var.origin_domain
    origin_id   = "EC2Origin"

    custom_origin_config {
      http_port              = 80    # OpenWebUI用のポートを80に変更
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "EC2Origin"

    forwarded_values {
      query_string = true
      headers      = ["*"]

      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}

# EC2のセキュリティグループにCloudFrontからの通信を許可するルールを追加
resource "aws_security_group_rule" "cloudfront_to_ec2" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]  # CloudFrontのIP範囲は動的に変更されるため
  security_group_id = var.security_group_id
  description       = "Allow CloudFront to OpenWebUI port"
}
