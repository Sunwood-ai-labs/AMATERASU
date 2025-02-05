# IPセットの作成（ホワイトリスト用）
resource "aws_wafv2_ip_set" "whitelist" {
  provider           = aws.virginia
  name               = "${var.project_name}-whitelist"
  description        = "Whitelisted IP addresses"
  scope              = "CLOUDFRONT"
  ip_address_version = "IPV4"
  addresses          = [
    "122.132.45.194/32",
    "93.118.41.103/32",
    "122.135.202.17/32",
    "93.118.41.105/32",
    "54.92.45.126/32",
    "35.79.202.92/32",
    "57.180.80.237/32",
    "52.195.98.19/32"
  ]

  tags = {
    Name = "${var.project_name}-whitelist"
  }
}

# WAFv2 Web ACLの作成（CloudFront用）
resource "aws_wafv2_web_acl" "cloudfront_waf" {
  provider    = aws.virginia
  name        = "${var.project_name}-cloudfront-waf"
  description = "WAF for CloudFront distribution with IP whitelist"
  scope       = "CLOUDFRONT"

  default_action {
    block {}
  }

  rule {
    name     = "allow-whitelist-ips"
    priority = 1

    action {
      allow {}
    }

    statement {
      or_statement {
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.whitelist.arn
          }
        }
        statement {
          geo_match_statement {
            country_codes = ["US"]
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "AllowWhitelistIPsMetric"
      sampled_requests_enabled  = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name               = "CloudFrontWAFMetric"
    sampled_requests_enabled  = true
  }

  tags = {
    Name = "${var.project_name}-waf"
  }
}

# WAF Web ACLのARNを出力
output "waf_web_acl_arn" {
  value       = aws_wafv2_web_acl.cloudfront_waf.arn
  description = "ARN of the WAF Web ACL"
}
