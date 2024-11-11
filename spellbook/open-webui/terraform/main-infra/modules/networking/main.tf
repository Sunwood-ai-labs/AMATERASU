# VPCモジュール
module "vpc" {
  source = "./vpc"

  vpc_cidr           = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  project_name       = var.project_name
  aws_region         = var.aws_region
}

# セキュリティグループモジュール
module "security" {
  source = "./security"

  project_name  = var.project_name
  vpc_id        = module.vpc.vpc_id
  whitelist_ips = [for entry in local.whitelist_entries : entry.ip]
}

# ALBモジュール
module "alb" {
  source = "./alb"

  project_name         = var.project_name
  vpc_id              = module.vpc.vpc_id
  public_subnet_id    = module.vpc.public_subnet_id
  public_subnet_2_id  = module.vpc.public_subnet_2_id
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
