# CloudFrontディストリビューション
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_200"
  aliases             = ["${var.subdomain}.${var.domain}"]
  wait_for_deployment = false
  web_acl_id          = aws_wafv2_web_acl.main.arn
  default_root_object = ""

  origin {
    domain_name = var.alb_dns_name
    origin_id   = "ALBOrigin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-Origin-Verify"
      value = random_string.origin_secret.result
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ALBOrigin"
    compress         = true

    origin_request_policy_id = aws_cloudfront_origin_request_policy.custom.id
    cache_policy_id          = aws_cloudfront_cache_policy.custom.id

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.cloudfront.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}

# カスタムオリジンリクエストポリシー
resource "aws_cloudfront_origin_request_policy" "custom" {
  name    = "${var.project_name}-custom-origin-request-policy"
  comment = "Policy for forwarding all headers and query strings"
  
  cookies_config {
    cookie_behavior = "all"
  }
  
  headers_config {
    header_behavior = "allViewer"
  }
  
  query_strings_config {
    query_string_behavior = "all"
  }
}

# カスタムキャッシュポリシー
resource "aws_cloudfront_cache_policy" "custom" {
  name        = "${var.project_name}-custom-cache-policy"
  comment     = "Policy for caching with custom settings"
  default_ttl = 0
  max_ttl     = 0
  min_ttl     = 0
  
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "none"
    }
    query_strings_config {
      query_string_behavior = "none"
    }
  }
}
