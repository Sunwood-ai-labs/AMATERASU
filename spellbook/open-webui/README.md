<div align="center">

![Open WebUI Infrastructure](assets/header.svg)

# Open WebUI Infrastructure

Modern infrastructure setup for Open WebUI deployment using Docker and AWS

</div>

## 🌟 概要

このプロジェクトはOpen WebUIのインフラストラクチャをTerraformとDockerを使用して構築するためのものです。セキュリティを重視したAWSリソースの自動プロビジョニングとコンテナ化されたアプリケーション環境を提供します。

## 📦 構成要素

```plaintext
├─ terraform/               # インフラストラクチャコード
│  ├─ main-infrastructure/ # メインのインフラ設定
│  │  ├─ modules/        # 各種モジュール
│  │  │  ├─ compute/    # EC2インスタンス管理
│  │  │  ├─ networking/ # ネットワーク設定
│  │  │  └─ iam/       # IAM権限管理
├─ docker-compose.yaml     # コンテナ化された環境設定
├─ .env.example           # 環境変数のテンプレート
```

## 🔒 セキュリティ機能

### アクセス制御
- **CloudFront + WAFv2**による多層防御
  - IPホワイトリストによる制限
  - レート制限とDDoS保護
  - カスタムルールセットの適用

### ネットワークセキュリティ
- **セキュリティグループの階層化**
  - ホワイトリスト用SG
  - CloudFront用SG
  - VPC内部通信用SG

### 内部通信
- **プライベートDNS**によるサービス間通信
  - 内部ドメイン: `sunwood-ai-labs-internal.com`
  - EC2インスタンスの自動DNS名解決
  - VPC内でのセキュアな通信

## 🛠️ セットアップ

1. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

2. インフラストラクチャのデプロイ
```bash
cd terraform/main-infrastructure
# terraform.tfvarsを設定
cp terraform.example.tfvars terraform.tfvars
# デプロイ実行
terraform init
terraform plan
terraform apply
```

3. アプリケーションの起動
```bash
docker-compose up -d
```

## 🔍 動作確認

### 接続確認スクリプト
提供されているPythonスクリプトで各種接続を確認できます：
```bash
python3 scripts/connectivity_health_check.py
```

このスクリプトは以下を確認します：
- DNS名前解決
- PING疎通確認
- HTTP接続確認
- レスポンスの内容確認

### 手動確認
1. プライベートDNSの動作確認
```bash
# VPC内のEC2インスタンスから実行
curl http://<subdomain>.sunwood-ai-labs-internal.com
```

2. セキュリティグループの確認
```bash
# ホワイトリストIPからのアクセス確認
curl https://<subdomain>.sunwood-ai-labs.com
```

## ⚙️ 設定オプション

### 環境変数

- `OPEN_WEBUI_PORT`: WebUIのポート番号（デフォルト: 8282）

### Terraform変数

主要な設定パラメータ（`terraform.tfvars`）：
```hcl
# プロジェクト設定
project_name = "amts-open-webui"
instance_type = "t3.medium"

# ドメイン設定
domain_internal = "sunwood-ai-labs-internal.com"
subdomain = "amaterasu-open-web-ui"
```

## 📝 トラブルシューティング

1. DNS解決の問題
- プライベートDNSの設定を確認
- Route53のレコードを確認

2. アクセス制限の問題
- WAFルールセットを確認
- IPホワイトリストを確認
- セキュリティグループの設定を確認

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
