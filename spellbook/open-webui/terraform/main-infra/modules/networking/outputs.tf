# VPCの出力
output "vpc_id" {
  description = "ID of the VPC"
  value       = data.aws_vpc.existing.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = data.aws_subnet.public_1.id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = data.aws_subnet.public_2.id
}

# セキュリティグループの出力
output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = module.security.ec2_security_group_id
}

output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = module.security.alb_security_group_id
}

# ALBの出力
output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = module.alb.alb_target_group_arn
}

output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = module.alb.alb_dns_name
}

output "alb_target_group_name" {
  description = "Name of the ALB target group"
  value       = module.alb.alb_target_group_name
}
