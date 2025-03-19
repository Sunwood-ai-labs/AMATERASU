<div align="center">

![Supabase Infrastructure](assets/header.svg)

# 🌟 Supabase Self-hosting インフラストラクチャ

Terraformを使用したSupabaseのセルフホスティング環境の構築とCloudFrontによるCDN配信の自動化

</div>

## 🎯 概要

このプロジェクトは、AWS上でSupabaseをセルフホスティングするための完全な Infrastructure as Code (IaC) ソリューションを提供します。TerraformとDockerを使用して、安全で拡張性の高いインフラストラクチャを自動的に構築します。

## 🏗️ アーキテクチャ

プロジェクトは以下の主要コンポーネントで構成されています：

- 📦 **Supabase Self-hosting**
  - PostgreSQLデータベース
  - Auth, Storage, Edge Functionsなどのサービス
  - 管理用ダッシュボード

- 🌐 **CDN配信**
  - CloudFrontによる高速なコンテンツ配信
  - WAFによるセキュリティ制御
  - カスタムドメイン対応

## 🚀 クイックスタート

### 前提条件

- AWS CLI設定済み
- Terraform v0.12以上
- Docker & Docker Compose

### セットアップ手順

1. 環境変数の設定：
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

2. インフラストラクチャのデプロイ：
```bash
cd terraform/main-infrastructure
terraform init
terraform plan
terraform apply
```

3. CDNの設定：
```bash
cd ../cloudfront-infrastructure
terraform init
terraform plan
terraform apply
```

4. アプリケーションの起動：
```bash
docker compose up -d
```

## 📁 プロジェクト構造

```plaintext
.
├── terraform/
│   ├── cloudfront-infrastructure/  # CDN関連の設定
│   └── main-infrastructure/        # 基本インフラの設定
├── example/                       # サンプル実装とテストデータ
│   └── README.md                  # テストデータのセットアップガイド
├── .env.example                   # 環境変数テンプレート
├── docker-compose.yml            # Supabaseサービス定義
└── reset.sh                      # 環境リセットスクリプト
```

テストデータのセットアップについては、[example/README.md](example/README.md)を参照してください。

## ⚙️ 設定項目

### 環境変数（.env）

- `POSTGRES_PASSWORD`: データベースパスワード
- `JWT_SECRET`: JWTシークレットキー
- `ANON_KEY`: 匿名アクセス用キー
- `SERVICE_ROLE_KEY`: サービスロール用キー

### Terraform変数（terraform.tfvars）

- `aws_region`: AWSリージョン
- `project_name`: プロジェクト名
- `domain`: ドメイン名
- `subdomain`: サブドメイン

## 🛠️ 開発ガイド

### リセット方法

環境を完全にリセットする場合：
```bash
./reset.sh
```

### カスタマイズ

1. CloudFront設定の変更：
   - `terraform/cloudfront-infrastructure/variables.tf`を編集

2. インフラ構成の変更：
   - `terraform/main-infrastructure/main.tf`を編集

## 📝 注意事項

- 本番環境では必ず`.env`の機密情報を変更してください
- CloudFrontのデプロイには15-30分程度かかる場合があります
- データベースのバックアップを定期的に行うことを推奨します

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能開発用のブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 📄 ライセンス

MIT
