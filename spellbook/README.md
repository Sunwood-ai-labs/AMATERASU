# AMATERASU Spellbook

AWS上にLLMプラットフォームをデプロイするためのInfrastructure as Code (IaC)コンポーネント群

## 📚 ディレクトリ構成

```
spellbook/
├── base-infrastructure/     # 基本AWS インフラ設定
├── langfuse/               # Langfuse 監視設定
├── litellm/               # LiteLLM プロキシ設定
├── open-webui/            # Open WebUI デプロイメント
└── open-webui-pipeline/   # WebUI パイプライン設定
```

## 🏗 コンポーネント

### ベースインフラストラクチャ

基本インフラストラクチャモジュールは以下のAWSリソースをセットアップします：

- パブリック/プライベートサブネットを持つVPC
- セキュリティグループとアクセス制御
- IAMロールとポリシー
- ネットワークルーティングとインターネットアクセス

`base-infrastructure/terraform.tfvars`での設定例：
```hcl
aws_region = "ap-northeast-1"
project_name = "amts-base-infrastructure" 
vpc_cidr = "10.0.0.0/16"
```

### Langfuse

LLMアプリケーションの監視・可観測性プラットフォーム：

- コスト追跡と分析
- モデルパフォーマンスモニタリング
- 利用状況メトリクスとダッシュボード

セットアップ（`langfuse/docker-compose.yml`）：
```bash
cd spellbook/langfuse
docker-compose up -d
```

### LiteLLM

統合LLM APIアクセスのためのプロキシサービス：

- モデルルーティングとロードバランシング
- 認証とレート制限
- 使用状況の追跡とモニタリング

`litellm/config.yaml`での設定例：
```yaml
model_list:
  - model_name: "bedrock/claude-3-5-sonnet"
    litellm_params:
      model: "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
```

### Open WebUI

LLMモデルと対話するためのWebインターフェース：

- モデル管理とテスト
- インタラクティブなチャットインターフェース
- API統合と設定

インフラストラクチャオプション：
- Main: CloudFront CDNを使用したフル機能デプロイメント
- Mini: テスト/開発用の簡易デプロイメント

## 🚀 デプロイメント

1. ベースインフラストラクチャ
```bash
cd spellbook/base-infrastructure
terraform init
terraform apply
```

2. Open WebUI デプロイメント
   
A. 標準デプロイメント（推奨）
```bash
# メインインフラストラクチャのみ
cd spellbook/open-webui/terraform/main-infrastructure
terraform init
terraform apply
```

B. カスタムデプロイメント（オプション）
```bash
# ミニインフラストラクチャ + CloudFront
cd spellbook/open-webui/terraform/mini-infrastructure
terraform init
terraform apply

cd ../cloudfront
terraform init
terraform apply
```

3. サービス
```bash
# Langfuseのデプロイ
cd spellbook/langfuse
docker-compose up -d

# LiteLLMのデプロイ
cd spellbook/litellm
docker-compose up -d

# Open WebUIのデプロイ
cd spellbook/open-webui
docker-compose up -d
```

## ⚙️ 設定

1. 各インフラストラクチャディレクトリの`whitelist.csv`でアクセス制御を設定
2. `litellm/config.yaml`でモデルエンドポイントを設定
3. `.env.example`を参考に`.env`ファイルで環境変数を設定

## 🔒 セキュリティ

- IPホワイトリストによるアクセス制御
- CloudFront/ALB経由のSSL/TLS暗号化
- 最小権限アクセスのIAMロール
- セキュリティグループによるネットワーク分離

## 📝 変数設定

terraform.tfvarsでの主要な設定変数：

```hcl
aws_region = "ap-northeast-1"
project_name = "amaterasu"
instance_type = "t3.medium"
domain = "your-domain.com"
```

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. プルリクエストを提出

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細はLICENSEファイルを参照してください。