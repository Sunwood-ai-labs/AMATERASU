# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0fde6326ce23fcb11"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-07ccf2ba130266f91"
public_subnet_2_id = "subnet-035f1861e57534990"
security_group_id  = "sg-01155c11cf80de6bc"  # 更新
ami_id             = "ami-0d52744d6551d851e"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"

# ドメイン設定
domain_internal    = "sunwood-ai-labs-internal.com"  # 内部ドメイン
route53_internal_zone_id = "Z09366661CLT9PAXECKAS"  # 更新
subdomain          = "amaterasu-litellm"

# プロジェクト設定パラメータ
project_name       = "amts-litellm"
instance_type      = "t3.medium"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
