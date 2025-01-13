output "default_security_group_id" {
  description = "ID of the default security group"
  value       = aws_security_group.default.id
}

output "whitelist_security_group_id" {
  description = "ID of the whitelist security group"
  value       = aws_security_group.whitelist.id
}

output "cloudfront_security_group_id" {
  description = "ID of the CloudFront security group"
  value       = aws_security_group.cloudfront.id
}

output "vpc_internal_security_group_id" {
  description = "ID of the VPC internal security group"
  value       = aws_security_group.vpc_internal.id
}
