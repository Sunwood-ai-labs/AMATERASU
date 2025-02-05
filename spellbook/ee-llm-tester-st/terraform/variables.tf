variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

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

variable "security_group_ids" {
  description = "List of security group IDs"
  type        = list(string)
}

# EC2インスタンス関連
variable "ecs_ami_id" {
  description = "AMI ID for ECS EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

# アプリケーション関連
variable "container_image" {
  description = "Container image to deploy"
  type        = string
}

variable "app_count" {
  description = "Number of application instances to run"
  type        = number
  default     = 1
}

# WAF関連
variable "whitelist_csv_path" {
  description = "Path to the CSV file containing whitelisted IP addresses"
  type        = string
}

variable "ec2_key_name" {
  description = "Name of the EC2 key pair"
  type        = string
}
