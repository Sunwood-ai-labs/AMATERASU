# terraform.tfvars
# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0013fddff64e654d1"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-005bc82dcd4ebe9cb"
public_subnet_2_id = "subnet-0937330dcc20e3a1f"
security_group_id  = "sg-09afd6eb5ab5cb990"
ami_id             = "ami-0d52744d6551d851e"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain             = "sunwood-ai-labs.click"

# プロジェクト設定パラメータ
project_name       = "amts-langfuse"
instance_type      = "t3.medium"
subdomain          = "amaterasu-langfuse-dev"

# ローカルファイルパス
env_file_path      = "C:/Prj/AMATERASU/spellbook/langfuse/.env"
setup_script_path  = "C:/Prj/AMATERASU/spellbook/langfuse/terraform/main-infrastructure/scripts/setup_script.sh"
