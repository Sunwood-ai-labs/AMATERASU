# outputs.tf
output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.id
}

output "cloudfront_arn" {
  description = "ARN of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.arn
}

output "cloudfront_status" {
  description = "Current status of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.status
}

output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = var.alb_dns_name
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = var.instance_id
}

output "instance_private_ip" {
  description = "Private IP of the EC2 instance"
  value       = var.instance_private_ip
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = var.instance_public_ip
}
