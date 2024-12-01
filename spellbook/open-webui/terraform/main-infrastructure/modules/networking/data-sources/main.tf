# modules/networking/data-sources/main.tf

# 既存のVPCを参照
data "aws_vpc" "existing" {
  id = var.vpc_id

  state = "available"  # VPCが利用可能な状態であることを確認
}

# 既存のパブリックサブネットを参照
data "aws_subnet" "public_1" {
  id = var.public_subnet_id

  state = "available"  # サブネットが利用可能な状態であることを確認
}

data "aws_subnet" "public_2" {
  id = var.public_subnet_2_id

  state = "available"  # サブネットが利用可能な状態であることを確認
}

# 既存のRoute53パブリックゾーンの参照
data "aws_route53_zone" "main" {
  name         = var.domain
  private_zone = false
}
