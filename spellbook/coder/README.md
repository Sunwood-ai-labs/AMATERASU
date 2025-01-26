<p align="center">
  <img src="./assets/header.png" alt="Coder Header" width="100%">
</p>

<h1 align="center">🌟 AMATERASU Spellbook - Coder</h1>

<p align="center">
  <a href="https://github.com/coder/coder/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/coder/coder?color=3AB2E6&style=for-the-badge">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/minimum-coder/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/minimum-coder?color=3AB2E6&style=for-the-badge">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/minimum-coder/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Sunwood-ai-labs/minimum-coder?color=3AB2E6&style=for-the-badge">
  </a>
</p>

<p align="center">
  <img alt="Terraform" src="https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white">
  <img alt="AWS" src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
  <img alt="VS Code" src="https://img.shields.io/badge/VS%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white">
</p>

[Coder](https://github.com/coder/coder)をベースにしたクラウド開発環境プラットフォームです。AWSインフラストラクチャを活用して、セキュアでスケーラブルなリモート開発環境を提供します。

## 💡 概要

このプロジェクトは以下の機能を提供します：

- 🏗️ Terraformを使用したAWSインフラストラクチャの自動構築
- 🌐 CloudFrontを活用した高速なグローバルコンテンツ配信
- 🔒 WAFとACMによるセキュアな通信
- 🚀 Docker Composeによる簡単な環境セットアップ

## 🏗️ インフラストラクチャ

プロジェクトは2つの主要なTerraformモジュールで構成されています：

### メインインフラストラクチャ (`terraform/main-infrastructure/`)
- 基本的なAWSリソースの管理
- 環境変数による設定管理
- スクリプトによる自動セットアップ

### CloudFrontインフラストラクチャ (`terraform/cloudfront-infrastructure/`)
- CloudFrontディストリビューションの設定
- Route 53によるDNS管理
- ACM証明書の自動管理
- WAFルールの設定

## ⚙️ 必要要件

- AWS CLI
- Terraform
- Docker & Docker Compose
- VS Code または他の互換性のあるIDE

## 📦 セットアップ

1. AWSクレデンシャルの設定：
```bash
aws configure
```

2. Terraformの初期化と適用：
```bash
# メインインフラストラクチャ
cd terraform/main-infrastructure
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply

# CloudFrontインフラストラクチャ
cd ../cloudfront-infrastructure
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply
```

3. Docker環境の起動：
```bash
docker-compose up -d
```

## 🔧 設定

### 環境変数
- メインインフラストラクチャの設定は `.env` ファイルで管理
- CloudFrontの設定は `terraform.tfvars` で管理

### インフラストラクチャの設定
- `main.tf` - 主要なリソース定義
- `variables.tf` - 変数定義
- `outputs.tf` - 出力値の定義

## 🤝 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📚 参考リンク

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Documentation](https://aws.amazon.com/documentation/)
- [Docker Documentation](https://docs.docker.com/)
- [Coder Documentation](https://coder.com/docs/coder-oss)
