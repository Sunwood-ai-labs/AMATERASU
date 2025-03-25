# Common variables that will be passed to the common module
variable "project_name" {
  description = "Name of the project"
  type        = string
}

# Common module reference
module "common" {
  source = "../common"

  # Required variables
  project_name = var.project_name
  
  # Optional variables with default values
  aws_region        = "ap-northeast-1"
  vpc_id            = ""
  vpc_cidr          = ""
  public_subnet_id  = ""
  public_subnet_2_id = ""
  domain            = ""
  subdomain         = ""
}

# Local variables using common module outputs
locals {
  name_prefix = module.common.name_prefix
  tags        = module.common.tags
}
