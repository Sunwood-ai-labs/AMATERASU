<div align="center">

![Base Infrastructure Header](assets/header.svg)

# Base Infrastructure Module

AMATERASUプロジェクトの基盤となるAWSインフラストラクチャを管理します。

</div>

## 🌟 概要

このモジュールは、以下のコアインフラストラクチャコンポーネントを提供します：

- VPC設定とネットワーキング
- セキュリティグループ管理
- Route53プライベートホストゾーン
- IPホワイトリスト管理

## 📦 モジュール構成

```plaintext
.
├── modules/
│   ├── vpc/              # VPCとネットワーク設定
│   ├── security/         # セキュリティグループと管理
│   └── route53/         # DNS設定
├── main.tf              # メインの設定ファイル
├── variables.tf         # 変数定義
└── outputs.tf          # 出力定義
```

## 🚀 デプロイメント手順

1. 環境変数の設定
```bash
# AWS認証情報の設定
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="ap-northeast-1"
```

2. `terraform.tfvars`の設定
```hcl
aws_region   = "ap-northeast-1"
project_name = "amts-base-infrastructure"
environment  = "dev"
vpc_cidr     = "10.0.0.0/16"
```

3. ホワイトリストIPの設定
```bash
cp whitelist.example.csv whitelist.csv
# whitelist.csvを編集
```

4. インフラストラクチャのデプロイ
```bash
terraform init
terraform plan
terraform apply
```

## 🔒 セキュリティ設定

### デフォルトセキュリティグループルール
- インバウンド：
  - SSH (22): ホワイトリストIPのみ
  - HTTP (80): ホワイトリストIPのみ
  - HTTPS (443): ホワイトリストIPのみ
  - その他のポート: VPC内部通信のみ許可
- アウトバウンド：
  - すべての通信を許可

### WAFとCloudFront設定
- IPベースのアクセス制御
- カスタムルールセット
- 地域制限オプション

### SSL/TLS証明書管理
- ACMによる証明書管理
- 自動更新設定
- マルチドメイン対応

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
