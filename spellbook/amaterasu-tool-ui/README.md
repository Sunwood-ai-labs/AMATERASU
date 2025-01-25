# 🎮 Amaterasu Tool

AWSインフラストラクチャの設定を管理するためのCLIツール

## 🚀 インストール

```bash
pip install -e .
```

## 📝 使用方法

基本的な使用方法:
```bash
# すべてのプロジェクトのterraform.tfvars生成
amaterasu --key-name AMATERASU-terraform-keypair-tokyo-PEM

# 特定のプロジェクトのみ処理
amaterasu --key-name AMATERASU-terraform-keypair-tokyo-PEM --project-dir litellm

# プロジェクトプレフィックスを指定して実行
amaterasu --key-name AMATERASU-terraform-keypair-tokyo-PEM --project-prefix my-prefix

# カスタム設定での実行
amaterasu \
  --key-name AMATERASU-terraform-keypair-tokyo-PEM \
  --instance-type t3.small \
  --base-path /custom/path/to/spellbook
```

## ⚙️ オプション

- `--base-path`: spellbookのベースディレクトリパス（デフォルト: /home/maki/prj/AMATERASU/spellbook）
- `--output-json`: output.jsonへのパス（デフォルト: base-infrastructure/output.json）
- `--project-dir`: 特定のプロジェクトの指定
- `--aws-region`: AWSリージョン（デフォルト: ap-northeast-1）
- `--instance-type`: EC2インスタンスタイプ（デフォルト: t3.micro）
- `--ami-id`: AMI ID（デフォルト: ami-0bba69335379e17f8）
- `--key-name`: SSH キーペア名（必須）
- `--project-prefix`: プロジェクト名のプレフィックス（デフォルト: amts-）

## 📄 生成される設定例

```hcl
# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0dc0e55990825027a"  # 既存のVPC ID
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-039f674c07c3c866c"  # 第1パブリックサブネット
public_subnet_2_id = "subnet-0103226f9ff80f7b0"  # 第2パブリックサブネット

# セキュリティグループID
security_group_ids = [
    "sg-0f1ee0363589d2a69",   # デフォルトセキュリティグループ
    "sg-0507b896c22985f03",   # CloudFrontセキュリティグループ
    "sg-0d3e1c55ee27a3e6c",   # VPC内部通信用セキュリティグループ
    "sg-0d0ce9672deda8220"    # ホワイトリストセキュリティグループ
]

# ドメイン設定
domain_internal    = "sunwood-ai-labs-internal.com"  # 内部ドメイン
route53_internal_zone_id = "Z0469656RKBUT8TGNNDQ"  # 内部ゾーンID
subdomain          = "amaterasu-litellm"

# プロジェクト設定パラメータ
project_name       = "amts-litellm"
instance_type      = "t3.micro"
ami_id             = "ami-0bba69335379e17f8"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
```

## 🔄 動作の流れ

1. base-infrastructure/output.jsonから既存の設定値を読み込み
2. プロジェクトディレクトリを探索
3. terraform.tfvarsファイルを生成
   - プロジェクト名とプレフィックスから自動的にサブドメインを生成
   - セキュリティグループ、サブネット、VPC情報を設定
   - ドメイン設定とRoute53ゾーン情報を設定
   - main-infrastructure と cloudfront-infrastructure の両方の terraform.tfvars を生成

## ⚠️ 注意事項

- `output.json`が存在しない場合はデフォルト値が使用されます
- サブドメインはプロジェクト名からプレフィックスを削除して生成されます
- キーペア名は必須パラメータです

## 📄 ライセンス

MIT License
