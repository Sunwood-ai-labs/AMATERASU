# modules/networking/route53/outputs.tf

output "private_zone_id" {
  description = "ID of the private hosted zone"
  value       = aws_route53_zone.private.id
}

output "public_record_fqdn" {
  description = "FQDN of the public DNS record"
  value       = aws_route53_record.public.fqdn
}

output "private_record_fqdn" {
  description = "FQDN of the private DNS record"
  value       = aws_route53_record.private.fqdn
}
