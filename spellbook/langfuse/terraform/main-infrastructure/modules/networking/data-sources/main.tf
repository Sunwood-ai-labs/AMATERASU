# データソースの定義

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

# 既存のRoute53ゾーンの参照
data "aws_route53_zone" "main" {
  name         = var.domain
  private_zone = false
}
