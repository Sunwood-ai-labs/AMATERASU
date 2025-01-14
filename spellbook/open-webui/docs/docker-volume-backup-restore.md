# 🌟 Open WebUI & Ollama のバックアップ・リストアガイド

## 📋 前提条件
- Docker Composeが実行可能な環境
- `docker-compose.yml` が設定済み
- `./backup` ディレクトリが存在すること

## 💾 バックアップ手順

### 🔷 Open WebUIのバックアップ
1. Open WebUIコンテナに接続
```bash
docker compose exec open-webui /bin/bash
```

2. データディレクトリに移動してバックアップを作成
```bash
cd /app/backend/data
tar czf /backup/openwebui-backup_$(date '+%Y%m%d_%H%M').tar.gz *
```

### 🔷 Ollamaのバックアップ
1. Ollamaコンテナに接続
```bash
docker compose exec ollama /bin/bash
```

2. データディレクトリに移動してバックアップを作成
```bash
cd /root/.ollama
tar czf /backup/ollama-backup_$(date '+%Y%m%d_%H%M').tar.gz *
```

## 🔄 リストア手順

### 🔶 Open WebUIのリストア
1. Open WebUIコンテナに接続
```bash
docker compose exec open-webui /bin/bash
```

2. データディレクトリで復元（TIMESTAMPは実際のバックアップファイルの日時）
```bash
cd /app/backend/data
tar xzf /backup/openwebui-backup_TIMESTAMP.tar.gz --overwrite
```

### 🔶 Ollamaのリストア
1. サービスを停止
```bash
docker compose down
```

2. Ollamaコンテナに接続
```bash
docker compose exec ollama /bin/bash
```

3. データディレクトリで復元（TIMESTAMPは実際のバックアップファイルの日時）
```bash
cd /root/.ollama
tar xzf /backup/ollama-backup_TIMESTAMP.tar.gz --overwrite
```

4. サービスを再起動
```bash
docker compose up -d
```

## ⚠️ 注意事項
- バックアップファイル名には自動的に日時が付与されます（形式：YYYYMMDD_HHMM）
- リストア時は必ず正しいタイムスタンプのファイルを指定してください
- 重要なデータは定期的にバックアップすることを推奨します
- バックアップファイルは安全な場所に保管してください
- リストア後はアプリケーションが正常に動作することを確認してください

## 📁 バックアップファイルの形式
- Open WebUI: `openwebui-backup_YYYYMMDD_HHMM.tar.gz`
- Ollama: `ollama-backup_YYYYMMDD_HHMM.tar.gz`

## 🔍 トラブルシューティング
- リストアが反映されない場合は、コンテナの再起動を試してください
- 圧縮ファイルが破損している場合は、別のバックアップファイルを使用してください
- パーミッションエラーが発生した場合は、コンテナ内で適切な権限があることを確認してください
