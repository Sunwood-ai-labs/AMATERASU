<div align="center">

![](assets/header.svg)

[![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue?logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v2.0%2B-blue?logo=docker)](https://docs.docker.com/compose/)
[![GitLab CE](https://img.shields.io/badge/GitLab%20CE-最新版-orange?logo=gitlab)](https://about.gitlab.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Maintained](https://img.shields.io/badge/メンテナンス-実施中-green.svg)](https://github.com/username/repo/graphs/commit-activity)

### 📋 概要

GitLab CEをDocker Composeで自己ホスティングするための設定リポジトリです。

</div>



## 🚀 クイックスタート

### 前提条件
- Docker 20.10以上
- Docker Compose v2.0以上
- 最小システム要件：
  - CPU: 4コア
  - メモリ: 8GB以上
  - ストレージ: 50GB以上

### セットアップ手順

1. リポジトリのクローン:
```bash
git clone <repository-url>
cd <repository-name>
```

2. 環境設定:
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

3. GitLabの起動:
```bash
docker compose up -d
```

## 💾 バックアップと復元

### バックアップの作成
```bash
# バックアップの実行
docker-compose exec gitlab gitlab-backup create

# バックアップファイルの確認
ls -la ./backups/

# バックアップファイルの確認（コンテナ内）
docker-compose exec gitlab ls -la /var/opt/gitlab/backups/
```

### バックアップの復元
1. GitLabサービスを停止:
```bash
docker-compose down
```

2. バックアップファイルの権限を設定:
```bash
sudo chmod 777 -R ./backups/
```

3. GitLabサービスを起動:
```bash
docker-compose up -d
```

4. バックアップを復元:
```bash
docker-compose exec gitlab gitlab-backup restore BACKUP=<バックアップ名>
```

## 🔧 トラブルシューティング

### ログの確認
```bash
docker compose logs gitlab
docker compose logs gitlab-runner
```

### システムステータスの確認
```bash
docker compose ps
```

## ⚠️ 注意事項
- 初回起動時は、GitLabの初期化に数分かかる場合があります
- システムリソースの使用状況を定期的に監視することをお勧めします
- 定期的なバックアップの実行を推奨します
