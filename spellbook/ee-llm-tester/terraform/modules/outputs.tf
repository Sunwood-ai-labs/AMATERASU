# CloudFront関連の出力
output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.main.id
  description = "The ID of the CloudFront distribution"
}

output "cloudfront_domain_name" {
  value       = aws_cloudfront_distribution.main.domain_name
  description = "The domain name of the CloudFront distribution"
}

# ECS関連の出力
output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = aws_ecs_service.app.name
  description = "The name of the ECS service"
}

# セキュリティグループ関連の出力
output "ecs_tasks_security_group_id" {
  value       = aws_security_group.ecs_tasks.id
  description = "The ID of the ECS tasks security group"
}

output "alb_security_group_id" {
  value       = aws_security_group.alb.id
  description = "The ID of the ALB security group"
}
