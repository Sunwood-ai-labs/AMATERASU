# CSVファイルからホワイトリストを読み込む
locals {
  whitelist_csv = file("${path.root}/../../whitelist-waf.csv")
  whitelist_lines = [for l in split("\n", local.whitelist_csv) : trim(l, " \t\r\n") if trim(l, " \t\r\n") != "" && !startswith(trim(l, " \t\r\n"), "ip")]
  whitelist_entries = [
    for l in local.whitelist_lines : {
      ip          = trim(element(split(",", l), 0), " \t\r\n")
      description = trim(element(split(",", l), 1), " \t\r\n")
    }
  ]
}

# IPセットの作成（ホワイトリスト用）
resource "aws_wafv2_ip_set" "whitelist" {
  provider           = aws.virginia
  name               = "${var.project_name}-whitelist"
  description        = "Whitelisted IP addresses from CSV"
  scope              = "CLOUDFRONT"
  ip_address_version = "IPV4"
  addresses          = [for entry in local.whitelist_entries : "${entry.ip}"]

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
