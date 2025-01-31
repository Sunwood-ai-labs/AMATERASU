# AWSプロバイダーの設定
provider "aws" {
  region = var.aws_region
}

# CloudFront/WAF用のバージニアリージョンプロバイダー
provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

# 変数をモジュールに渡す
locals {
  common_vars = {
    project_name        = var.project_name
    aws_region         = var.aws_region
    vpc_id            = var.vpc_id
    vpc_cidr          = var.vpc_cidr
    public_subnet_id  = var.public_subnet_id
    public_subnet_2_id = var.public_subnet_2_id
    container_image   = var.container_image
    app_count        = var.app_count
    whitelist_csv_path = var.whitelist_csv_path
    ecs_ami_id       = var.ecs_ami_id
    instance_type    = var.instance_type
    ec2_key_name     = var.ec2_key_name
  }
}

# メインのモジュール参照
module "main" {
  source = "./modules"
  
  providers = {
    aws          = aws
    aws.virginia = aws.virginia
  }

  project_name      = local.common_vars.project_name
  aws_region        = local.common_vars.aws_region
  vpc_id           = local.common_vars.vpc_id
  vpc_cidr         = local.common_vars.vpc_cidr
  public_subnet_id = local.common_vars.public_subnet_id
  public_subnet_2_id = local.common_vars.public_subnet_2_id
  container_image  = local.common_vars.container_image
  app_count        = local.common_vars.app_count
  whitelist_csv_path = local.common_vars.whitelist_csv_path
  ecs_ami_id      = local.common_vars.ecs_ami_id
  instance_type   = local.common_vars.instance_type
  ec2_key_name    = local.common_vars.ec2_key_name
}
