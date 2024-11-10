provider "aws" {
  region = var.aws_region
}

# CloudFront用のACM証明書はus-east-1リージョンに作成する必要があります
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}
