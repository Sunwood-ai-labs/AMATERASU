# GitLab Runner セットアップガイド

このガイドでは、GitLabのCI/CDパイプライン実行のためのGitLab Runnerの設定方法について説明します。

## 📋 前提条件

- GitLabが正常に動作していること
- Docker Composeが設定済みであること
- GitLabの管理者権限があること

## 🚀 Runner のセットアップ

### 1. Docker Compose 設定

既存のdocker-compose.ymlファイルにRunner設定が含まれていることを確認します：

```yaml
gitlab-runner:
  image: gitlab/gitlab-runner:latest
  restart: always
  volumes:
    - './runner:/etc/gitlab-runner'
    - /var/run/docker.sock:/var/run/docker.sock
```

### 2. Registration Token の取得

1. GitLabのWeb UIにアクセス
2. Admin Area > Runners に移動
3. 「New instance runner」をクリック
4. 表示されたRegistration tokenをコピー

### 3. Runnerの登録

#### コンテナの起動
```bash
# Runnerコンテナを起動
docker compose up -d gitlab-runner
```

#### Runnerの登録
```bash
# Runnerコンテナに接続
docker compose exec gitlab-runner bash

# Runner登録コマンドを実行
gitlab-runner register
```

登録時の入力情報：

| 入力項目 | 設定値 | 説明 |
|----------|--------|------|
| GitLab instance URL | http://gitlab | Docker Compose内部でのサービス名を使用 |
| Registration token | [コピーしたトークン] | GitLab UIで取得したトークン |
| Description | docker-runner | Runner の説明（任意） |
| Tags | docker | ジョブで使用するタグ |
| Executor | docker | 実行環境として Docker を使用 |
| Default Docker image | docker:latest | デフォルトのDockerイメージ |

#### 登録の確認
```bash
# 登録されたRunnerの一覧を表示
gitlab-runner list
```

## 📝 CI/CD パイプラインの設定

### 基本的な .gitlab-ci.yml の例

```yaml
image: docker:latest

services:
  - docker:dind

stages:
  - build
  - test

build:
  stage: build
  tags:
    - docker  # 登録時に指定したタグ
  script:
    - echo "Building the project..."
    - docker info

test:
  stage: test
  tags:
    - docker
  script:
    - echo "Running tests..."
```

### カスタムDockerイメージを使用する例

```yaml
image: node:16

stages:
  - build
  - test

build:
  stage: build
  tags:
    - docker
  script:
    - npm install
    - npm run build

test:
  stage: test
  tags:
    - docker
  script:
    - npm run test
```

## ⚙️ Runner の詳細設定

### コンテナ設定のカスタマイズ

`/etc/gitlab-runner/config.toml` の設定例：

```toml
[[runners]]
  name = "docker-runner"
  url = "http://gitlab"
  token = "YOUR-TOKEN"
  executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = true
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
```

### キャッシュの設定

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .npm/
```

## 🔍 トラブルシューティング

### よくある問題と解決方法

1. **Runner が登録できない**
   ```bash
   # GitLabとRunnerの接続を確認
   docker compose exec gitlab-runner ping gitlab
   ```

2. **ジョブが開始されない**
   ```bash
   # Runnerのログを確認
   docker compose logs gitlab-runner
   ```

3. **Docker in Docker が動作しない**
   ```bash
   # privileged モードが有効か確認
   docker compose exec gitlab-runner docker info
   ```

### ログの確認方法

```bash
# Runnerの詳細ログを表示
docker compose exec gitlab-runner gitlab-runner --debug run

# Runner のステータス確認
docker compose exec gitlab-runner gitlab-runner status
```

## 📊 ベストプラクティス

1. **タグの効果的な使用**
   - 環境ごとに異なるタグを使用
   - 目的別のRunnerを区別

2. **リソース制限の設定**
   ```toml
   [runners.docker]
     cpus = "2"
     memory = "2g"
   ```

3. **セキュリティ考慮事項**
   - 機密情報はCI/CD変数として設定
   - privilegedモードは必要な場合のみ有効化

4. **キャッシュ戦略**
   - 依存関係のキャッシュ
   - ビルドアーティファクトの効率的な管理

## 🔄 メンテナンス

### Runnerの更新
```bash
# イメージの更新
docker compose pull gitlab-runner

# コンテナの再起動
docker compose up -d gitlab-runner
```

### 定期的なチェック
- Runner のステータス監視
- ジョブ履歴の確認
- リソース使用状況の監視

### クリーンアップ
```bash
# 未使用のイメージ削除
docker compose exec gitlab-runner docker system prune -a

# キャッシュのクリア
docker compose exec gitlab-runner gitlab-runner cache clean
```
