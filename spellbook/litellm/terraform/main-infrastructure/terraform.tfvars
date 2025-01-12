# terraform.tfvars
# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0dc8cb87d464edc77"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-0d92d159dda7f5688"
public_subnet_2_id = "subnet-0d3144797a2f55895"
security_group_id  = "sg-0f16ffea1167ec5ba"
ami_id             = "ami-0d52744d6551d851e"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain             = "sunwood-ai-labs.com"

# プロジェクト設定パラメータ
project_name       = "amts-litellm"
instance_type      = "t3.medium"
subdomain          = "amaterasu-litellm"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
