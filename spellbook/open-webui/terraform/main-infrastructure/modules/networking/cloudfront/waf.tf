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

  # テスト用に一時的にWAFルールを無効化

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.project_name}-waf-metrics"
    sampled_requests_enabled   = true
  }
}
