terraform {
  required_version = ">= 0.12"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "local" {
    path = "terraform.tfstate"
  }
}

# デフォルトプロバイダー設定
provider "aws" {
  region = var.aws_region
}

# バージニアリージョン用のプロバイダー設定（CloudFront用）
provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

# CloudFrontモジュールの呼び出し
module "cloudfront" {
  source = "./modules"

  project_name      = var.project_name
  aws_region        = var.aws_region
  origin_domain     = var.origin_domain
  domain            = var.domain
  subdomain         = var.subdomain

  providers = {
    aws           = aws
    aws.virginia = aws.virginia
  }
}
