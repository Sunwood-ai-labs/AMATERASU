# ALB関連の出力
output "alb_dns_name" {
  value       = module.alb.alb_dns_name
  description = "The DNS name of the Application Load Balancer"
}

# アプリケーションURL
output "app_url" {
  value       = module.alb.app_url
  description = "The HTTPS URL of the deployed application"
}

# ECS関連の出力
output "ecs_cluster_name" {
  value       = module.alb.ecs_cluster_name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = module.alb.ecs_service_name
  description = "The name of the ECS service"
}

# Route53関連の出力
output "route53_record_name" {
  value       = module.alb.route53_record_name
  description = "The name of the Route53 record"
}

# セキュリティグループ関連の出力
output "alb_security_group_id" {
  value       = module.alb.alb_security_group_id
  description = "The ID of the ALB security group"
}

output "ecs_tasks_security_group_id" {
  value       = module.alb.ecs_tasks_security_group_id
  description = "The ID of the ECS tasks security group"
}
