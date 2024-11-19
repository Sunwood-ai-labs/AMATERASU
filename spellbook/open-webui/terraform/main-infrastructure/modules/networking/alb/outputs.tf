# spellbook/open-webui/terraform/main-infrastructure/modules/networking/alb/outputs.tf

output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = aws_lb_target_group.main.arn
}

output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "The canonical hosted zone ID of the ALB"
  value       = aws_lb.main.zone_id
}

output "alb_target_group_name" {
  description = "Name of the ALB target group"
  value       = aws_lb_target_group.main.name
}