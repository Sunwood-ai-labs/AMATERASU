# CloudFront Distribution
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled    = true
  price_class        = "PriceClass_200"
  comment            = "${var.project_name} distribution"

  origin {
    domain_name = "${replace(aws_ecs_service.app.name, "-service", "")}.${var.project_name}.local"
    origin_id   = "ECS"

    custom_origin_config {
      http_port              = 80
      https_port             = 80
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-Origin-Verify"
      value = random_string.origin_verify.result
    }
  }

  # オリジン認証用のランダム文字列
  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ECS"

    forwarded_values {
      query_string = true
      headers      = ["Host", "Origin"]
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0  # キャッシュを無効化
    max_ttl                = 0  # キャッシュを無効化
  }

  ordered_cache_behavior {
    path_pattern     = "/_stcore/*"  # Streamlitの静的アセット
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ECS"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400    # 24時間
    max_ttl                = 31536000 # 1年
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

# オリジン認証用のランダム文字列を生成
resource "random_string" "origin_verify" {
  length  = 32
  special = false
}

# 出力定義
output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.main.id
  description = "The ID of the CloudFront distribution"
}

output "cloudfront_domain_name" {
  value       = aws_cloudfront_distribution.main.domain_name
  description = "The domain name of the CloudFront distribution"
}
