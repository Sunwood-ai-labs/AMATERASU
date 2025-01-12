# Default configuration
terraform {
    required_version = ">= 0.12"
    
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = "~> 4.0"
        }
    }
    }

    provider "aws" {
    region = var.aws_region
    }

    locals {
    whitelist_csv = file("${path.root}/whitelist-base-sg.csv")
    whitelist_lines = [for l in split("\n", local.whitelist_csv) : trim(l, " \t\r\n") if trim(l, " \t\r\n") != "" && !startswith(trim(l, " \t\r\n"), "ip")]
    whitelist_entries = [
        for l in local.whitelist_lines : {
        ip          = trim(element(split(",", l), 0), " \t\r\n")
        description = trim(element(split(",", l), 1), " \t\r\n")
        }
    ]
}
