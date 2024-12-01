output "zone_id" {
  description = "ID of the Route53 private hosted zone"
  value       = aws_route53_zone.private.zone_id
}

output "zone_name" {
  description = "Name of the Route53 private hosted zone"
  value       = aws_route53_zone.private.name
}