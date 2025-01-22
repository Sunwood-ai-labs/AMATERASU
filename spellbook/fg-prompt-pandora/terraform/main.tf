# AWSプロバイダーの設定
provider "aws" {
  region = var.aws_region
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
    security_group_ids = var.security_group_ids
    container_image  = var.container_image
    task_cpu         = var.task_cpu
    task_memory      = var.task_memory
    app_count        = var.app_count
  }
}

# ECSモジュールの参照
module "ecs" {
  source = "./modules"
  
  project_name      = local.common_vars.project_name
  aws_region        = local.common_vars.aws_region
  vpc_id           = local.common_vars.vpc_id
  vpc_cidr         = local.common_vars.vpc_cidr
  public_subnet_id = local.common_vars.public_subnet_id
  public_subnet_2_id = local.common_vars.public_subnet_2_id
  security_group_ids = local.common_vars.security_group_ids
  container_image  = local.common_vars.container_image
  task_cpu         = local.common_vars.task_cpu
  task_memory      = local.common_vars.task_memory
  app_count        = local.common_vars.app_count
}
