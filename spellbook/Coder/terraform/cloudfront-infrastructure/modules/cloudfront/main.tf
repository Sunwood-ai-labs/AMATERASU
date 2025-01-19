# CloudFrontディストリビューション設定
resource "aws_cloudfront_distribution" "main" {
  provider = var.providers.aws
  enabled             = true
  is_ipv6_enabled    = true
  price_class        = "PriceClass_200"
  retain_on_delete   = false
  wait_for_deployment = false
  web_acl_id         = aws_wafv2_web_acl.cloudfront_waf.arn
  aliases            = ["${var.subdomain}.${var.domain}"]

  origin {
    domain_name = var.origin_domain
    origin_id   = "EC2Origin"

    custom_origin_config {
      http_port              = 80
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
    acm_certificate_arn = aws_acm_certificate.cloudfront_cert.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method = "sni-only"
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}
