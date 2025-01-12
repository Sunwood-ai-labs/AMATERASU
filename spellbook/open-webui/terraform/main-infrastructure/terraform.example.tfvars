# terraform.tfvars.example
# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-xxxxxxxxxxxxxxxxx"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-xxxxxxxxxxxxxxxxx"
public_subnet_2_id = "subnet-xxxxxxxxxxxxxxxxx"
security_group_id  = "sg-xxxxxxxxxxxxxxxxx"
ami_id             = "ami-xxxxxxxxxxxxxxxxx"
key_name           = "your-key-pair-name"
domain             = "example.com"

# プロジェクト設定パラメータ
project_name       = "project-name"
instance_type      = "t3.medium"
subdomain          = "your-subdomain"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
