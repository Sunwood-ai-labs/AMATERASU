# Common variables that will be passed to the common module
variable "project_name" {
  description = "Name of the project"
  type        = string
}

# Compute specific variables
variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
}

variable "iam_instance_profile" {
  description = "Name of the IAM instance profile"
  type        = string
}

variable "security_group_id" {
  description = "ID of the security group"
  type        = string
}

# 環境変数ファイルのパス
variable "env_file_path" {
  description = "Absolute path to the .env file"
  type        = string
}

# セットアップスクリプトのパス
variable "setup_script_path" {
  description = "Absolute path to the setup_script.sh file"
  type        = string
}

# Required variables from common module
variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "ID of the public subnet"
  type        = string
}

# プライベートIPアドレス
variable "private_ip_address" {
  description = "Fixed private IP address for the instance"
  type        = string
  default     = null  # デフォルトはnullで、自動割り当てを許可
}

# Common module reference
module "common" {
  source = "../common"

  # Required variables
  project_name      = var.project_name
  
  # Optional variables with default values
  aws_region        = "ap-northeast-1"
  vpc_id            = var.vpc_id
  vpc_cidr          = var.vpc_cidr
  public_subnet_id  = var.public_subnet_id
  public_subnet_2_id = ""
  domain            = ""
  subdomain         = ""
}

# Local variables using common module outputs
locals {
  name_prefix = module.common.name_prefix
  tags        = module.common.tags
}
