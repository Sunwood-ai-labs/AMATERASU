# Route 53 ゾーンの参照
data "aws_route53_zone" "selected" {
  name = var.domain
}

# Route 53 レコードの作成
resource "aws_route53_record" "app" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# 出力定義
output "app_url" {
  value       = "https://${var.subdomain}.${var.domain}"
  description = "The HTTPS URL of the deployed application"
}

output "route53_record_name" {
  value       = aws_route53_record.app.name
  description = "The name of the Route53 record"
}
