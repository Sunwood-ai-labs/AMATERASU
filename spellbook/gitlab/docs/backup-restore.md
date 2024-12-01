# GitLab バックアップ・復元ガイド

このガイドでは、Docker ComposeでホストされているGitLabのバックアップと復元の詳細な手順を説明します。

## 📋 バックアップ

### バックアップの種類

GitLabのバックアップには以下のデータが含まれます：
- データベース
- レポジトリ
- GitLab設定
- CI/CD環境設定
- Issues、MergeRequests等のメタデータ
- アップロードされたファイル

### バックアップの実行

#### 1. 手動バックアップの作成

```bash
# バックアップの実行（タイムスタンプ付きのバックアップファイルが作成されます）
docker compose exec gitlab gitlab-backup create

# バックアップファイルの確認（ホストOS上）
ls -la ./backups/

# バックアップファイルの確認（コンテナ内）
docker compose exec gitlab ls -la /var/opt/gitlab/backups/
```

#### 2. 自動バックアップの設定

Docker Compose設定ファイルの`GITLAB_OMNIBUS_CONFIG`に以下を追加：

```yaml
environment:
  GITLAB_OMNIBUS_CONFIG: |
    # バックアップの保存期間を7日に設定
    gitlab_rails['backup_keep_time'] = 604800
    
    # バックアップのスケジュール設定（毎日午前2時）
    gitlab_rails['backup_upload_connection'] = {
      'provider' => 'local',
      'local_root' => '/var/opt/gitlab/backups'
    }
```

#### 3. バックアップファイルの保管

重要なバックアップファイルは別の場所にコピーすることを推奨：

```bash
# バックアップファイルを安全な場所にコピー
cp ./backups/[timestamp]_gitlab_backup.tar /path/to/secure/storage/

# AWS S3への同期例
aws s3 sync ./backups/ s3://your-bucket/gitlab-backups/
```

## 🔄 復元

### 前提条件の確認

- GitLabのバージョンがバックアップ時と同じか確認
- 十分なディスク容量があることを確認
- 実行前にテスト環境での復元を推奨

### 復元手順

#### 1. GitLabサービスの停止

```bash
# GitLabサービスを停止
docker compose down
```

#### 2. バックアップファイルの準備

```bash
# バックアップファイルのパーミッション設定
sudo chmod 777 -R ./backups/

# 必要に応じてバックアップファイルを配置
cp /path/to/backup/[timestamp]_gitlab_backup.tar ./backups/
```

#### 3. GitLabサービスの起動と復元

```bash
# GitLabサービスを起動
docker compose up -d

# システムが完全に起動するまで待機（約2-3分）
sleep 180

# バックアップからの復元を実行
docker compose exec gitlab gitlab-backup restore BACKUP=[timestamp]
```

#### 4. 復元の確認

```bash
# GitLabのログを確認
docker compose logs gitlab

# システムの状態を確認
docker compose ps
```

## ⚠️ 注意事項

### バックアップに関する注意

- バックアップ実行中はパフォーマンスに影響が出る可能性があります
- バックアップファイルのサイズは定期的に監視してください
- 古いバックアップは自動的に削除されます（設定した保存期間に基づく）

### 復元に関する注意

- 復元プロセスは既存のデータを上書きします
- 復元中はGitLabサービスが利用できません
- 大規模なデータの場合、復元に時間がかかる場合があります

## 🔍 トラブルシューティング

### バックアップ失敗時

1. ディスク容量の確認：
```bash
df -h
```

2. パーミッションの確認：
```bash
ls -la ./backups/
```

3. GitLabのログ確認：
```bash
docker compose logs gitlab | grep backup
```

### 復元失敗時

1. バックアップファイルの整合性確認：
```bash
tar tf [timestamp]_gitlab_backup.tar
```

2. GitLabのバージョン確認：
```bash
docker compose exec gitlab cat /opt/gitlab/version-manifest.txt
```

3. 詳細なログの確認：
```bash
docker compose exec gitlab gitlab-ctl tail
```

## 📊 バックアップ管理のベストプラクティス

1. **定期的なバックアップテスト**
   - 月1回程度、テスト環境での復元を実施
   - バックアップデータの整合性チェック

2. **バックアップの分散保管**
   - 本番環境とは別の場所にバックアップを保存
   - できれば異なるリージョンやクラウドプロバイダーも利用

3. **バックアップ運用の自動化**
   - バックアップスクリプトの作成
   - 監視とアラートの設定

4. **ドキュメント管理**
   - バックアップと復元手順の文書化
   - 実行ログの保管
