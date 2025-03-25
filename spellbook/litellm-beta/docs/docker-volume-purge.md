# Docker Volumeのパージ手順書

## 概要
本ドキュメントでは、Docker Composeで作成されたボリューム（postgres_data、prometheus_data）を安全にパージ（完全削除）する手順について説明します。

## 前提条件
- Docker Composeがインストールされていること
- 対象のDockerサービスが実行中または停止中であること
- sudo権限を持っていること

## 構成
対象のボリューム：
- postgres_data（PostgreSQLデータ用）
- prometheus_data（Prometheusメトリクス用）

## パージ手順

### 1. 事前準備
作業を開始する前に、以下の注意点を確認してください：
- データベースやメトリクスの重要なデータがある場合は、事前にバックアップを取得してください
- 運用環境での実行は、メンテナンス時間帯に実施することを推奨します

### 2. サービスの停止
まず、実行中のコンテナを停止します：
```bash
sudo docker-compose down
```

### 3. ボリュームの削除
以下のいずれかの方法でボリュームを削除できます：

#### 方法1：個別削除
特定のボリュームのみを削除する場合：
```bash
sudo docker volume rm postgres_data
sudo docker volume rm prometheus_data
```

#### 方法2：一括削除
プロジェクトの全てのボリュームを一括で削除する場合：
```bash
sudo docker-compose down -v
```

### 4. 削除の確認
ボリュームが正しく削除されたことを確認します：
```bash
sudo docker volume ls
```

### 5. サービスの再開
必要に応じて、サービスを再起動します：
```bash
sudo docker-compose up -d
```
新しいボリュームが自動的に作成され、サービスが開始されます。

## トラブルシューティング

### ボリュームが削除できない場合
1. 使用中のコンテナがないか確認：
```bash
sudo docker ps -a
```

2. 関連するコンテナを強制削除：
```bash
sudo docker rm -f <container_id>
```

3. 再度ボリュームの削除を試行

## 注意事項
- ボリュームを削除すると、保存されていたデータは完全に失われます
- 運用環境での実行前に、必要なデータのバックアップを必ず取得してください
- システムの重要度に応じて、メンテナンス時間帯での実施を検討してください
