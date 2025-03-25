# Common variable definitions

# プロジェクト名（全リソースの接頭辞として使用）
variable "project_name" {
  description = "Name of the project (used as a prefix for all resources)"
  type        = string
}

# AWSリージョン
variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "ap-northeast-1"
}

# 既存のVPC ID
variable "vpc_id" {
  description = "ID of the existing VPC"
  type        = string
}

# VPCのCIDRブロック
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

# 第1パブリックサブネットのID
variable "public_subnet_id" {
  description = "ID of the first public subnet"
  type        = string
}

# 第2パブリックサブネットのID
variable "public_subnet_2_id" {
  description = "ID of the second public subnet"
  type        = string
}

# セキュリティグループID
variable "security_group_ids" {
  description = "List of security group IDs to attach to the instance"
  type        = list(string)
}

# ベースドメイン名
variable "domain" {
  description = "Base domain name for the application"
  type        = string
  default     = "sunwood-ai-labs.click"
}

# サブドメインプレフィックス
variable "subdomain" {
  description = "Subdomain prefix for the application"
  type        = string
  default     = "amaterasu-open-web-ui-dev"
}

# プライベートホストゾーンのドメイン名
variable "domain_internal" {
  description = "Domain name for private hosted zone"
  type        = string
}

# Route53のゾーンID
variable "route53_internal_zone_id" {
  description = "Zone ID for Route53 private hosted zone"
  type        = string
}

# EC2インスタンス関連の変数
# EC2インスタンスのAMI ID
variable "ami_id" {
  description = "AMI ID for the EC2 instance (defaults to Ubuntu 22.04 LTS)"
  type        = string
  default     = "ami-0d52744d6551d851e"  # Ubuntu 22.04 LTS in ap-northeast-1
}

# EC2インスタンスタイプ
variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
  default     = "t3.medium"
}

# SSHキーペア名
variable "key_name" {
  description = "Name of the SSH key pair for EC2 instance"
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

# 共通のローカル変数
locals {
  # リソース命名用の共通プレフィックス
  name_prefix = "${var.project_name}-"
  
  # 完全修飾ドメイン名
  fqdn = "${var.subdomain}.${var.domain}"
  
  # 共通タグ
  common_tags = {
    Project     = var.project_name
    Environment = terraform.workspace
    ManagedBy   = "terraform"
  }
}
