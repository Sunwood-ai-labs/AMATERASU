resource "aws_route53_record" "private_http" {
  zone_id = var.route53_zone_id
  name    = "${var.subdomain}.${var.domain_internal}"
  type    = "CNAME"
  ttl     = 300
  records = [var.instance_private_dns]
}

output "private_dns_info" {
  description = "Private DNS information for HTTP access"
  value = {
    domain_name = "${var.subdomain}.${var.domain_internal}"
    record_type = "CNAME"
    ttl         = 300
    target      = var.instance_private_dns
  }
}
