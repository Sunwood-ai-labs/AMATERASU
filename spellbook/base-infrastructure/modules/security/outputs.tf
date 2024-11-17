# modules/security/outputs.tf

output "default_security_group_id" {
  description = "ID of the default security group"
  value       = aws_security_group.default.id
}
