variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
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
