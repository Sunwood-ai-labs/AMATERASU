# GitLab Docker Compose Setup

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
- AWS Systems Manager Session Manager（SSHアクセス用）

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

4. 初期rootパスワードの取得:
```bash
docker compose exec gitlab cat /etc/gitlab/initial_root_password
```

## 📚 詳細ガイド

- [SSH設定ガイド](docs/ssh-setup.md) - GitLabへのSSHアクセス設定
- [バックアップ・復元ガイド](docs/backup-restore.md) - バックアップと復元手順
- [Runner設定ガイド](docs/runner-setup.md) - GitLab RunnerのCI/CD設定
- 
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

## 📑 Docker Compose 設定

```yaml
version: '3.6'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest'
    restart: always
    hostname: 'amaterasu-gitlab-dev.sunwood-ai-labs.click'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://amaterasu-gitlab-dev.sunwood-ai-labs.click'
        gitlab_rails['time_zone'] = 'Asia/Tokyo'
        gitlab_rails['backup_keep_time'] = 604800
    ports:
      - '80:80'
      - '443:443'
      - '2222:22'
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
      - './backups:/var/opt/gitlab/backups'
    shm_size: '256m'

  gitlab-runner:
    image: gitlab/gitlab-runner:latest
    restart: always
    volumes:
      - './runner:/etc/gitlab-runner'
      - /var/run/docker.sock:/var/run/docker.sock
```
