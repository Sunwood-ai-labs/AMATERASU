
<div align="center">

![Open WebUI Infrastructure](assets/header.svg)

# Dify 簡易セットアップガイド

</div>

<div align="center">

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

</div>

このガイドでは、Difyを最小限の設定で素早く起動する方法を説明します。

## ⚙️ 前提条件

- Docker がインストールされていること
- Docker Compose がインストールされていること

## インストール手順

1. Dockerディレクトリに移動します：
```bash
cd docker
```

2. 環境設定ファイルを作成します：
```bash
cp .env.example .env
```

3. 必要なディレクトリを作成します（初回のみ）：
```bash
mkdir -p ./volumes/db/data
```

4. サービスを起動します：
```bash
docker compose up -d
```

## アクセス方法

- Web UI: `http://localhost:80`
- API エンドポイント: `http://localhost:80/api`

## ⚡ デフォルト設定

データベース接続情報：
- ホスト: localhost
- ポート: 5432
- データベース名: dify
- ユーザー名: postgres
- パスワード: difyai123456

## 🔧 トラブルシューティング

エラーが発生した場合は、以下の手順を試してください：

1. ログの確認：
```bash
docker compose logs
```

2. サービスの再起動：
```bash
docker compose restart
```

3. クリーンインストール：
```bash
# すべてを停止
docker compose down

# データを削除
rm -rf ./volumes/*

# 再インストール
docker compose up -d
```

## 🛠️ メンテナンス

- サービスの停止：
```bash
docker compose down
```

- サービスの起動：
```bash
docker compose up -d
```

- 特定のサービスの再起動：
```bash
docker compose restart [サービス名]
```

## ⚠️ 注意事項

- 初回起動時は、Dockerイメージのダウンロードに時間がかかる場合があります
- 本番環境で使用する場合は、セキュリティ設定の見直しを推奨します
- データのバックアップは定期的に行うことを推奨します

## 💬 サポート

問題が解決しない場合は、以下を確認してください：
- 公式ドキュメント: `https://docs.dify.ai`
- GitHubイシュー: `https://github.com/langgenius/dify/issues`

---
このREADMEは基本的な起動手順のみをカバーしています。より詳細な設定や本番環境での利用については、公式ドキュメントを参照してください。
