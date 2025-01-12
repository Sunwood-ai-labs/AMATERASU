variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "aws_region" {
  description = "AWS region for the resources"
  type        = string
  default     = "ap-northeast-1"
}

variable "origin_domain" {
  description = "Domain name of the origin (EC2 instance)"
  type        = string
}

variable "vpc_id" {
  description = "ID of the existing VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "ID of the public subnet"
  type        = string
}

variable "security_group_id" {
  description = "ID of the existing security group"
  type        = string
}

variable "allowed_ip_ranges" {
  description = "List of IP ranges to allow access to CloudFront (in CIDR notation)"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # デフォルトですべてのIPを許可（開発用）
}

variable "domain" {
  description = "メインドメイン名"
  type        = string
}

variable "subdomain" {
  description = "サブドメイン名"
  type        = string
}
