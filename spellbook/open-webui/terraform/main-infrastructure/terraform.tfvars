# terraform.tfvars
# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0c660c24a3058a48f"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-0d64af8e37f66597c"
public_subnet_2_id = "subnet-0c346c102abafa139"
security_group_id  = "sg-023d4ef2a650829e2"
ami_id             = "ami-0d52744d6551d851e"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain             = "sunwood-ai-labs.com"

# プロジェクト設定パラメータ
project_name       = "amts-open-webui"
instance_type      = "t3.medium"
subdomain          = "amaterasu-open-web-ui"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
