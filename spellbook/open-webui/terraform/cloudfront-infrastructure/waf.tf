# WAFv2 Web ACLの作成（CloudFront用）
resource "aws_wafv2_web_acl" "cloudfront_waf" {
  provider    = aws.virginia
  name        = "${var.project_name}-cloudfront-waf"
  description = "WAF for CloudFront distribution"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}  # デフォルトでアクセスを許可
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name               = "CloudFrontWAFMetric"
    sampled_requests_enabled  = true
  }
}