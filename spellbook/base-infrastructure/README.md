<div align="center">

![Base Infrastructure Header](assets/header.svg)

# Base Infrastructure Module

AMATERASUプロジェクトの基盤となるAWSインフラストラクチャを管理します。

</div>

## 🌟 概要

このモジュールは、以下のコアインフラストラクチャコンポーネントを提供します：

- [VPC設定とネットワーキング](#vpc設定)
- [セキュリティグループ管理](#セキュリティ設定)
- [Route53プライベートホストゾーン](#dns設定)
- [IPホワイトリスト管理](#ipホワイトリスト管理)

## 📦 モジュール構成

```plaintext
.
├── modules/
│   ├── vpc/              # VPCとネットワーク設定
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   ├── security/         # セキュリティグループと管理
│   │   ├── default.tf
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   └── route53/          # DNS設定
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── main.tf               # メインの設定ファイル
├── variables.tf          # 変数定義
├── outputs.tf           # 出力定義
└── terraform.tfvars      # 環境変数設定
```

### VPC設定
VPCリソースの定義は[main.tf](modules/vpc/main.tf)に、出力定義は[outputs.tf](modules/vpc/outputs.tf)に、変数定義は[variables.tf](modules/vpc/variables.tf)に記述されています。

### セキュリティ設定
デフォルトセキュリティグループの定義は[default.tf](modules/security/default.tf)に、セキュリティグループの定義は[main.tf](modules/security/main.tf)に、出力定義は[outputs.tf](modules/security/outputs.tf)に、変数定義は[variables.tf](modules/security/variables.tf)に記述されています。

### DNS設定
Route53リソースの定義は[main.tf](modules/route53/main.tf)に、出力定義は[outputs.tf](modules/route53/outputs.tf)に、変数定義は[variables.tf](modules/route53/variables.tf)に記述されています。

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

### デフォルトセキュリティグループルール (ID: sg-06ba6015aa88f338d)
- インバウンド：
  - SSH (22): ホワイトリストIPのみ
  - HTTP/HTTPS (80-443): CloudFrontプレフィックスリストからのアクセスを許可
  - その他のポート: VPC内部通信のみ許可
- アウトバウンド：
  - すべての通信を許可

>[!NOTE]  CloudFrontからのアクセスは、AWSのマネージドプレフィックスリスト（com.amazonaws.global.cloudfront.origin-facing）を使用して許可されています。これにより、CloudFrontの全エッジロケーションからのアクセスが単一のルールで管理されます。

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
