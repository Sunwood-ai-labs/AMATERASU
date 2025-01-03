<div align="center">

![Open WebUI Infrastructure](assets/header.svg)

# Open WebUI Infrastructure

Modern infrastructure setup for Open WebUI deployment using Docker and AWS

</div>

## 🌟 概要

このプロジェクトはOpen WebUIのインフラストラクチャをTerraformとDockerを使用して構築するためのものです。AWSリソースの自動プロビジョニングとコンテナ化されたアプリケーション環境を提供します。

## 📦 構成要素

```plaintext
├─ terraform/               # インフラストラクチャコード
│  ├─ main-infrastructure/ # メインのインフラ設定
│  ├─ cloudfront/         # CloudFront配信設定
├─ docker-compose.yaml     # コンテナ化された環境設定
├─ .env.example           # 環境変数のテンプレート
```

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

- CloudFrontによるコンテンツ配信
- WAFによるアクセス制御
- SSL/TLS暗号化（Let's Encrypt）
- セキュリティグループの自動設定
- VPC内の隔離された環境

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
