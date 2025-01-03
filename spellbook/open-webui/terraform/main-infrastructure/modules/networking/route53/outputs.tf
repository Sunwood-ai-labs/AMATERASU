output "public_internal_record_fqdn" {
  description = "The FQDN of the created internal public Route53 record"
  value       = aws_route53_record.public_internal.fqdn
}

output "private_record_fqdn" {
  description = "The FQDN of the created private Route53 record"
  value       = var.create_private_zone ? aws_route53_record.private[0].fqdn : null
}

output "private_zone_id" {
  description = "ID of the private hosted zone"
  value       = var.create_private_zone ? aws_route53_zone.private[0].id : null
}

output "public_internal_record_id" {
  description = "ID of the internal public Route53 A record"
  value       = aws_route53_record.public_internal.id
}

output "public_zone_id" {
  description = "ID of the public hosted zone"
  value       = data.aws_route53_zone.public.id
}

output "health_check_id" {
  description = "ID of the Route53 health check"
  value       = var.enable_health_check ? aws_route53_health_check.alb[0].id : null
}
