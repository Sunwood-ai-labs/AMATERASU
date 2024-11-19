output "dns_name" {
  description = "The DNS name of the created record"
  value       = "${var.subdomain}.${var.domain}"
}

output "record_name" {
  description = "The name of the created Route53 record"
  value       = aws_route53_record.alb.name
}

output "record_fqdn" {
  description = "The FQDN of the created Route53 record"
  value       = aws_route53_record.alb.fqdn
}

output "health_check_id" {
  description = "The ID of the created health check (if enabled)"
  value       = var.enable_health_check ? aws_route53_health_check.alb[0].id : null
}
