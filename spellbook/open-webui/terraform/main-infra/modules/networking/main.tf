# spellbook/open-webui/terraform/main-infra/modules/networking/main.tf
# 既存のVPCを参照
data "aws_vpc" "existing" {
  id = var.vpc_id
}

# 既存のパブリックサブネットを参照
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

# セキュリティグループモジュール
module "security" {
  source = "./security"

  project_name  = var.project_name
  vpc_id        = var.vpc_id
  whitelist_ips = [for entry in local.whitelist_entries : entry.ip]
}

# ALBモジュール
module "alb" {
  source = "./alb"

  project_name         = var.project_name
  vpc_id              = var.vpc_id
  public_subnet_id    = var.public_subnet_id
  public_subnet_2_id  = var.public_subnet_2_id
  alb_security_group_id = module.security.alb_security_group_id
}

locals {
  whitelist_csv = file("${path.root}/whitelist.csv")
  whitelist_lines = [for l in split("\n", local.whitelist_csv) : trim(l, " \t\r\n") if trim(l, " \t\r\n") != ""]
  whitelist_entries = [
    for l in slice(local.whitelist_lines, 1, length(local.whitelist_lines)) : {
      ip          = trim(element(split(",", l), 0), " \t\r\n")
      description = trim(element(split(",", l), 1), " \t\r\n")
    }
  ]
}
