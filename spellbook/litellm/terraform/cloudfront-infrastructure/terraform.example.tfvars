# terraform.example.tfvars
#--------------------------------------------------------------
# AWSの設定
#--------------------------------------------------------------
# リソースを作成するAWSリージョンを指定
# デフォルト: 東京リージョン
aws_region = "ap-northeast-1"

#--------------------------------------------------------------
# ネットワーク設定
#--------------------------------------------------------------
# VPC関連の設定
# 実際のVPC、サブネット、セキュリティグループIDに置き換えてください
vpc_id             = "vpc-xxxxxxxxxxxxxxxxx"  # 例: vpc-0a1b2c3d4e5f67890
public_subnet_id   = "subnet-xxxxxxxxxxxxxxxxx"  # 例: subnet-0a1b2c3d4e5f67890
security_group_id  = "sg-xxxxxxxxxxxxxxxxx"   # 例: sg-0a1b2c3d4e5f67890

#--------------------------------------------------------------
# プロジェクト設定
#--------------------------------------------------------------
# リソースのタグ付けと識別に使用するプロジェクト名
# 小文字、数字、ハイフンのみを使用してください
project_name = "your-project-name"  # 例: my-web-application

#--------------------------------------------------------------
# ドメイン設定
#--------------------------------------------------------------
# オリジンサーバー（EC2インスタンスドメインまたはALBドメイン）
origin_domain = "your-origin.example.com"  # 例: ec2-xx-xxx-xxx-xxx.compute.amazonaws.com

# ドメイン設定
# メインドメインはRoute53に登録されている必要があります
domain    = "example.com"         # 登録済みのドメイン
subdomain = "your-subdomain"      # 例: app（app.example.comが生成されます）