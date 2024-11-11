# main.tf
resource "aws_cloudfront_distribution" "main" {
  enabled = true
  
  origin {
    domain_name = "amts-open-webui-alb-977186521.ap-northeast-1.elb.amazonaws.com"  # ALBのドメイン名を直接指定
    origin_id   = "amts-open-webui-alb"  # ALBの名前を直接指定

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"  # ALBがHTTPで待ち受けている場合
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "amts-open-webui-alb"  # 上記のorigin_idと同じ値

    forwarded_values {
      query_string = true
      headers      = ["*"]  # 全てのヘッダーを転送
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0  # キャッシュを無効化
    max_ttl                = 0
  }

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "amts-open-webui-cloudfront"
  }
}
