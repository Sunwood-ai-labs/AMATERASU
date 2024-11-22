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

variable "public_subnet_id" {
  description = "ID of the first public subnet"
  type        = string
}

variable "public_subnet_2_id" {
  description = "ID of the second public subnet"
  type        = string
}

# セキュリティグループ
variable "security_group_id" {
  description = "ID of the existing security group"
  type        = string
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

# ドメイン関連
variable "domain" {
  description = "Domain name to use"
  type        = string
}

variable "subdomain" {
  description = "Subdomain to use"
  type        = string
}

# その他
variable "ami_id" {
  description = "ID of the AMI to use"
  type        = string
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
}
