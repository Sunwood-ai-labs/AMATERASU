output "certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = aws_acm_certificate.cert.arn
}

output "domain_validation_options" {
  description = "Domain validation options for the certificate"
  value       = aws_acm_certificate.cert.domain_validation_options
}

output "validation_record_fqdns" {
  description = "FQDNs of the validation records"
  value       = [for record in aws_route53_record.cert_validation : record.fqdn]
}

output "certificate_domain" {
  description = "Domain name for which the certificate was issued"
  value       = "${var.subdomain}.${var.domain}"
}

output "certificate_status" {
  description = "Status of the certificate validation"
  value       = aws_acm_certificate_validation.cert.id
}
