# modules/networking/alb/outputs.tf

output "alb_target_group_arn" {
  description = "ARN of the public ALB target group"
  value       = aws_lb_target_group.public.arn
}

output "alb_dns_name" {
  description = "DNS name of the public ALB"
  value       = aws_lb.public.dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the public ALB"
  value       = aws_lb.public.zone_id
}

output "alb_target_group_name" {
  description = "Name of the public ALB target group"
  value       = aws_lb_target_group.public.name
}

# インターナルALBの出力も追加
output "internal_alb_target_group_arn" {
  description = "ARN of the internal ALB target group"
  value       = aws_lb_target_group.internal.arn
}

output "internal_alb_dns_name" {
  description = "DNS name of the internal ALB"
  value       = aws_lb.internal.dns_name
}

output "internal_alb_zone_id" {
  description = "Zone ID of the internal ALB"
  value       = aws_lb.internal.zone_id
}
