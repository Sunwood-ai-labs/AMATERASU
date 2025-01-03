# ランダムな文字列を生成（Origin認証用）
resource "random_string" "origin_secret" {
  length  = 32
  special = false
}

# CSVファイルからIPアドレスを読み込む
locals {
  whitelist = csvdecode(file("${path.root}/whitelist..csv"))
  ip_addresses = [for entry in local.whitelist : entry.ip]
}

# WAF ACLの作成
resource "aws_wafv2_web_acl" "main" {
  provider    = aws.us_east_1
  name        = "${var.project_name}-waf"
  description = "WAF for CloudFront with IP whitelist"
  scope       = "CLOUDFRONT"

  default_action {
    block {
      custom_response {
        response_code = 403
        custom_response_body_key = "ip_block"
      }
    }
  }

  custom_response_body {
    key          = "ip_block"
    content      = "Access denied: Your IP is not in the whitelist"
    content_type = "TEXT_PLAIN"
  }

  rule {
    name     = "AllowWhitelistedIPs"
    priority = 1

    action {
      allow {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.whitelist.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "AllowWhitelistedIPsMetric"
      sampled_requests_enabled  = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name               = "${var.project_name}-waf-metrics"
    sampled_requests_enabled  = true
  }
}

# IPセットの作成
resource "aws_wafv2_ip_set" "whitelist" {
  provider           = aws.us_east_1
  name               = "${var.project_name}-ip-whitelist"
  description        = "Whitelisted IP addresses"
  scope              = "CLOUDFRONT"
  ip_address_version = "IPV4"
  addresses          = local.ip_addresses

  tags = {
    Name = "${var.project_name}-ip-whitelist"
  }
}
