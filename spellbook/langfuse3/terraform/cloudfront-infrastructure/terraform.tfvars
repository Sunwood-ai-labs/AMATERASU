#--------------------------------------------------------------
# AWSの設定
#--------------------------------------------------------------
# 東京リージョンを使用
aws_region = "ap-northeast-1"

#--------------------------------------------------------------
# プロジェクト設定
#--------------------------------------------------------------
# リソースのタグ付けと識別に使用するプロジェクト名
project_name = "amts-litellm"

#--------------------------------------------------------------
# ドメイン設定
#--------------------------------------------------------------
# オリジンサーバー（EC2インスタンス）
origin_domain = "ec2-35-76-63-147.ap-northeast-1.compute.amazonaws.com"

# ドメイン設定
domain     = "sunwood-ai-labs.com"
subdomain  = "amaterasu-litellm"  # 生成されるURL: amaterasu-litellm.sunwood-ai-labs.com
