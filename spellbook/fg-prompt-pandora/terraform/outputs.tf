# CloudFront関連の出力
output "cloudfront_distribution_id" {
  value       = module.ecs.cloudfront_distribution_id
  description = "The ID of the CloudFront distribution"
}

output "cloudfront_domain_name" {
  value       = module.ecs.cloudfront_domain_name
  description = "The domain name of the CloudFront distribution"
}

# ECS関連の出力
output "ecs_cluster_name" {
  value       = module.ecs.ecs_cluster_name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = module.ecs.ecs_service_name
  description = "The name of the ECS service"
}

# セキュリティグループ関連の出力
output "ecs_tasks_security_group_id" {
  value       = module.ecs.ecs_tasks_security_group_id
  description = "The ID of the ECS tasks security group"
}

output "nat_gateway_ip" {
  value       = module.ecs.nat_gateway_ip
  description = "The Elastic IP address of the NAT Gateway"
}
