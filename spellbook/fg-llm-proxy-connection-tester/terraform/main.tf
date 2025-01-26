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
    whitelist_csv_path = var.whitelist_csv_path
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
  whitelist_csv_path = local.common_vars.whitelist_csv_path
  global_accelerator_dns_name = aws_globalaccelerator_accelerator.main.dns_name
}

# グローバルアクセラレータの作成
resource "aws_globalaccelerator_accelerator" "main" {
  name            = "${var.project_name}-ga"
  enabled         = true
  ip_address_type = "IPV4"
}

# リスナーの作成
resource "aws_globalaccelerator_listener" "main" {
  accelerator_arn = aws_globalaccelerator_accelerator.main.id
  client_affinity = "NONE"
  protocol        = "TCP"

  port_range {
    from_port = 80
    to_port   = 80
  }
}

# エンドポイントグループの作成
resource "aws_globalaccelerator_endpoint_group" "main" {
  listener_arn = aws_globalaccelerator_listener.main.id

  endpoint_configuration {
    endpoint_id = module.ecs.alb_id
    weight      = 100
  }
}

output "global_accelerator_dns_name" {
  value = aws_globalaccelerator_accelerator.main.dns_name
  description = "Global Accelerator DNS Name"
}
