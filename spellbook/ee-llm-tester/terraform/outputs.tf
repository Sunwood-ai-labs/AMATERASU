# CloudFront関連の出力
output "cloudfront_distribution_id" {
  value       = module.main.cloudfront_distribution_id
  description = "The ID of the CloudFront distribution"
}

output "cloudfront_domain_name" {
  value       = module.main.cloudfront_domain_name
  description = "The domain name of the CloudFront distribution"
}

# ECS関連の出力
output "ecs_cluster_name" {
  value       = module.main.ecs_cluster_name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = module.main.ecs_service_name
  description = "The name of the ECS service"
}

# セキュリティグループ関連の出力
output "ecs_tasks_security_group_id" {
  value       = module.main.ecs_tasks_security_group_id
  description = "The ID of the ECS tasks security group"
}
