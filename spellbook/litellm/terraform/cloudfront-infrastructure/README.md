<div align="center">

![CloudFront Infrastructure](https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/spellbook/open-webui/terraform/cloudfront-infrastructure/assets/header.svg)

</div>

# AWS CloudFront Infrastructure Module

このリポジトリは、AWSのCloudFrontディストリビューションを設定するための再利用可能なTerraformモジュールを提供します。

## 🌟 主な機能

- ✅ CloudFrontディストリビューションの作成（カスタムドメイン対応）
- 🛡️ WAFv2によるIPホワイトリスト制御
- 🌐 Route53でのDNSレコード自動設定
- 🔒 ACM証明書の自動作成と検証

## 📁 ディレクトリ構造

```
cloudfront-infrastructure/
├── modules/
│   └── cloudfront/           # メインモジュール
│       ├── main.tf          # リソース定義
│       ├── variables.tf     # 変数定義
│       ├── outputs.tf       # 出力定義
│       └── README.md        # モジュールのドキュメント
└── examples/
    └── complete/            # 完全な使用例
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        ├── terraform.tfvars.example
        └── whitelist-waf.csv.example
```

## 🚀 クイックスタート

1. モジュールの使用例をコピーします：
```bash
cp -r examples/complete your-project/
cd your-project
```

2. 設定ファイルを作成します：
```bash
cp terraform.tfvars.example terraform.tfvars
cp whitelist-waf.csv.example whitelist-waf.csv
```

3. terraform.tfvarsを編集して必要な設定を行います：
```hcl
# AWSリージョン設定
aws_region = "ap-northeast-1"

# プロジェクト名
project_name = "your-project-name"

# オリジンサーバー設定（EC2インスタンス）
origin_domain = "your-ec2-domain.compute.amazonaws.com"

# ドメイン設定
domain    = "your-domain.com"
subdomain = "your-subdomain"
```

4. whitelist-waf.csvを編集してIPホワイトリストを設定します：
```csv
ip,description
192.168.1.1/32,Office Network
10.0.0.1/32,Home Network
```

5. Terraformを実行します：
```bash
terraform init
terraform plan
terraform apply
```

## 📚 より詳細な使用方法

より詳細な使用方法については、[modules/cloudfront/README.md](modules/cloudfront/README.md)を参照してください。

## 🔧 カスタマイズ

このモジュールは以下の要素をカスタマイズできます：

1. CloudFront設定
   - キャッシュ動作
   - オリジンの設定
   - SSL/TLS設定

2. WAF設定
   - IPホワイトリストの管理
   - セキュリティルールのカスタマイズ

3. DNS設定
   - カスタムドメインの設定
   - Route53との連携

## 📝 注意事項

- CloudFrontのデプロイには時間がかかる場合があります（15-30分程度）
- DNSの伝播には最大72時間かかる可能性があります
- SSL証明書の検証には数分から数十分かかることがあります
- WAFのIPホワイトリストは定期的なメンテナンスが必要です

## 🔍 トラブルシューティング

詳細なトラブルシューティングガイドについては、[modules/cloudfront/README.md](modules/cloudfront/README.md#トラブルシューティング)を参照してください。
