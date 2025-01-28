# プロジェクト名
variable "project_name" {
  description = "Name of the project"
  type        = string
}

# AWS リージョン
variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
}

# VPC関連
variable "vpc_id" {
  description = "ID of the existing VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

# サブネット（ECSタスク用）
variable "public_subnet_id" {
  description = "ID of the first public subnet for ECS tasks"
  type        = string
}

variable "public_subnet_2_id" {
  description = "ID of the second public subnet for ECS tasks"
  type        = string
}

# セキュリティグループ（CloudFrontアクセス用）
variable "security_group_ids" {
  description = "List of security group IDs for CloudFront access"
  type        = list(string)
}

# コンテナ関連
variable "container_image" {
  description = "Container image to deploy"
  type        = string
}

variable "task_cpu" {
  description = "CPU units for the task"
  type        = string
}

variable "task_memory" {
  description = "Memory (MiB) for the task"
  type        = string
}

variable "app_count" {
  description = "Number of application instances to run"
  type        = number
}

# WAF関連
variable "whitelist_csv_path" {
  description = "Path to the CSV file containing whitelisted IP addresses for CloudFront"
  type        = string
}
