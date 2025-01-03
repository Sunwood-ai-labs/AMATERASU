# ランダムな文字列を生成（Origin認証用）
resource "random_string" "origin_secret" {
  length  = 32
  special = false
}

# WAF ACLの作成
resource "aws_wafv2_web_acl" "main" {
  provider    = aws.us_east_1
  name        = "${var.project_name}-waf"
  description = "WAF for CloudFront"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}
  }

  # レートベースのルール
  rule {
    name     = "RateBasedRule"
    priority = 1

    override_action {
      none {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "RateBasedRuleMetric"
      sampled_requests_enabled  = true
    }
  }

  # AWS マネージドルール - 一般的な脆弱性対策
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
        version     = "Version_1.5"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "AWSManagedRulesCommonRuleSetMetric"
      sampled_requests_enabled  = true
    }
  }

  # SQLインジェクション対策
  rule {
    name     = "AWSManagedRulesSQLiRuleSet"
    priority = 3

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
        version     = "Version_1.0"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "AWSManagedRulesSQLiRuleSetMetric"
      sampled_requests_enabled  = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name               = "${var.project_name}-waf-metrics"
    sampled_requests_enabled  = true
  }

  tags = {
    Name = "${var.project_name}-waf"
  }
}

# CloudFront用のACM証明書（us-east-1リージョンに作成）
resource "aws_acm_certificate" "cloudfront" {
  provider          = aws.us_east_1
  domain_name       = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"

  tags = {
    Name = "${var.project_name}-cloudfront-cert"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# DNS検証用のレコードを作成
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.route53_zone_id
}

# 証明書の検証完了を待機
resource "aws_acm_certificate_validation" "cloudfront" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# CloudFrontディストリビューション
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled    = true
  price_class        = "PriceClass_200"
  aliases            = ["${var.subdomain}.${var.domain}"]
  wait_for_deployment = false
  web_acl_id         = aws_wafv2_web_acl.main.arn
  default_root_object = "index.html"

  origin {
    domain_name = var.alb_dns_name
    origin_id   = "ALBOrigin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "match-viewer"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    # カスタムヘッダーによる認証
    custom_header {
      name  = "X-Origin-Verify"
      value = random_string.origin_secret.result
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "ALBOrigin"
    compress         = true

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
    acm_certificate_arn      = aws_acm_certificate.cloudfront.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}

# CloudFront用のRoute53レコード
resource "aws_route53_record" "cloudfront" {
  zone_id         = var.route53_zone_id
  name            = "${var.subdomain}.${var.domain}"
  type            = "A"
  allow_overwrite = true

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }

  depends_on = [
    aws_cloudfront_distribution.main
  ]
}
