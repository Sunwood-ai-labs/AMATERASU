<div align="center">

![Open WebUI Infrastructure](assets/header.svg)

# Open WebUI Infrastructure

Modern infrastructure setup for Open WebUI deployment using Docker and AWS

</div>

## 🌟 概要

このプロジェクトはOpen WebUIのインフラストラクチャをTerraformとDockerを使用して構築するためのものです。AWSリソースの自動プロビジョニングとコンテナ化されたアプリケーション環境を提供します。

## 📦 構成要素

- `terraform/` - インフラストラクチャコードとモジュール
  - [Main Infrastructure](./terraform/main-infrastructure/README.md) - メインのインフラストラクチャ設定
  - [CloudFront Infrastructure](./terraform/cloudfront-infrastructure/README.md) - CloudFront配信設定
- `docker-compose.yaml` - コンテナ化された環境設定
- `.env.example` - 環境変数のテンプレート

詳細な設定とデプロイメント手順については[Terraform Infrastructure](./terraform/README.md)を参照してください。

## 🛠️ クイックスタート

1. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

2. アプリケーションの起動
```bash
docker-compose up -d
```

## ⚙️ 設定オプション

### 環境変数

- `OPEN_WEBUI_PORT`: WebUIのポート番号（デフォルト: 8282）

その他の設定オプションについては各インフラストラクチャモジュールのドキュメントを参照してください。

## 🔒 セキュリティ機能

- SSL/TLS暗号化（Let's Encrypt）
- セキュリティグループの自動設定
- WAFによる保護
- VPC内の隔離された環境

詳細なセキュリティ設定については[Main Infrastructure](./terraform/main-infrastructure/README.md)を参照してください。

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献ガイドライン

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成