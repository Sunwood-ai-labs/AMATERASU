<div align="center">

![Open WebUI Infrastructure](../../assets/header.svg)

# Main Infrastructure Module

Core infrastructure components for Open WebUI deployment

</div>

## 🎯 概要

Open WebUIのコアインフラストラクチャを管理するTerraformモジュールです。EC2、VPC、ALB、IAMなどの主要なAWSリソースを統合的に管理します。

## 📦 モジュール構成

### Common Module (`modules/common/`)
- プロジェクト全体で使用される変数と設定の定義
- タグ管理とリソース命名規則

### Compute Module (`modules/compute/`)
- EC2インスタンス管理
- 自動起動/停止スケジュール
- ボリューム設定

### IAM Module (`modules/iam/`)
- サービスロールとポリシー
- インスタンスプロファイル
- 最小権限の原則に基づく設定

### Networking Module (`modules/networking/`)
- VPC設定とサブネット管理
- ALBとターゲットグループ
- Route53 DNS管理
- ACM証明書

## 🛠️ デプロイメント手順

1. 環境変数の設定
```bash
# terraform.tfvarsを環境に合わせて編集
```

2. モジュールの初期化とデプロイ
```bash
terraform init
terraform plan
terraform apply
```

詳細な設定手順と変数については[親ディレクトリのREADME](../README.md)を参照してください。

## 📝 出力値

主要な出力値：

- VPC/サブネット情報
- EC2インスタンス詳細
- ALB設定
- DNS情報

## ⚠️ トラブルシューティング

よくある問題と解決方法については[CloudFront Infrastructure](../cloudfront-infrastructure/README.md)も併せて参照してください。