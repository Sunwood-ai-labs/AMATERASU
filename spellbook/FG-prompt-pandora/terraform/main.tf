# AWSプロバイダーの設定
provider "aws" {
  region = var.aws_region
}

# 既存のVPCを参照
data "aws_vpc" "existing" {
  id = var.vpc_id
}

# 既存のサブネットを参照
data "aws_subnet" "public_1" {
  id = var.public_subnet_id
}

data "aws_subnet" "public_2" {
  id = var.public_subnet_2_id
}

# 既存のセキュリティグループを参照
data "aws_security_group" "existing" {
  id = var.security_group_id
}

# 変数をモジュールに渡す
locals {
  common_vars = {
    project_name      = var.project_name
    aws_region        = var.aws_region
    vpc_id           = var.vpc_id
    vpc_cidr         = var.vpc_cidr
    public_subnet_id = var.public_subnet_id
    public_subnet_2_id = var.public_subnet_2_id
    security_group_id = var.security_group_id
    container_image  = var.container_image
    task_cpu         = var.task_cpu
    task_memory      = var.task_memory
    app_count        = var.app_count
    domain           = var.domain
    subdomain        = var.subdomain
    ami_id           = var.ami_id
    key_name         = var.key_name
  }
}

# モジュールの参照
module "alb" {
  source = "./modules"
  # 共通変数の設定
  project_name      = local.common_vars.project_name
  aws_region        = local.common_vars.aws_region
  vpc_id           = local.common_vars.vpc_id
  vpc_cidr         = local.common_vars.vpc_cidr
  public_subnet_id = local.common_vars.public_subnet_id
  public_subnet_2_id = local.common_vars.public_subnet_2_id
  security_group_id = local.common_vars.security_group_id
  container_image  = local.common_vars.container_image
  task_cpu         = local.common_vars.task_cpu
  task_memory      = local.common_vars.task_memory
  app_count        = local.common_vars.app_count
  domain           = local.common_vars.domain
  subdomain        = local.common_vars.subdomain
  ami_id           = local.common_vars.ami_id
  key_name         = local.common_vars.key_name
}
