# AWSリージョン
aws_region         = "ap-northeast-1"

# VPC設定
vpc_id             = "vpc-0fa210da8decf182e"
vpc_cidr           = "10.0.0.0/16"  
public_subnet_id   = "subnet-0302d7be4333bc65f"
public_subnet_2_id = "subnet-0c0cbf5b4cce1ba65"

# セキュリティグループ設定
security_group_ids = [
  "sg-028a8c1271c764aff",    # デフォルトセキュリティグループ
  "sg-0ee8d78feb33f9346",    # CloudFrontセキュリティグループ
  "sg-0c50e0c864fca32a8",    # VPC内部セキュリティグループ
  "sg-040d517cafc8c33b8"     # ホワイトリストセキュリティグループ
]

# Route53設定
domain           = "sunwood-ai-labs.com"       # パブリックドメイン
domain_internal  = "sunwood-ai-labs.internal"  # プライベートドメイン
route53_zone_id = "Z03859723B3G1JBAW267M"     # パブリックゾーンID
route53_internal_zone_id = "Z03877383MSPHSMX91Q8Y"  # プライベートゾーンID

# EC2インスタンス設定
ami_id             = "ami-0d52744d6551d851e"  # Ubuntu 22.04 LTS
key_name           = "your-key-pair-name"
instance_type      = "t3.medium"

# プロジェクト設定
project_name       = "amaterasu-litellm-beta"
environment        = "dev"
subdomain          = "litellm-beta"  # 結果: litellm-beta.sunwood-ai-labs.com

# アプリケーション設定
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"

# タグ設定
tags = {
  Environment = "dev"
  Project     = "amaterasu"
  ManagedBy   = "terraform"
}
