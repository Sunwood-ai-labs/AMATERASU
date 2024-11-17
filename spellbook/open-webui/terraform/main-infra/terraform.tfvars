# terraform.tfvars
aws_region         = "ap-northeast-1"
project_name       = "amts-open-webui"
vpc_id             = "vpc-0021a4e9c7c2641fc"               # 既存のVPC ID
vpc_cidr           = "10.0.0.0/16"                         # 既存のVPCのCIDR
public_subnet_id   = "subnet-0cd355401e0f0c039"            # 既存のpublic-subnet-1のID
public_subnet_2_id = "subnet-0089842ff56bae96d"            # 既存のpublic-subnet-2のID
public_subnet_cidr = "10.0.1.0/24"                         # 既存のパブリックサブネットのCIDR
security_group_id  = "sg-0e46c8154501d24e8"               # 既存のデフォルトセキュリティグループID
ami_id             = "ami-0d52744d6551d851e"               # Ubuntu 20.04 LTS
instance_type      = "t3.medium"                           # 2 vCPU, 4 GiB Memory
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain_name        = "cloudfront.net"
