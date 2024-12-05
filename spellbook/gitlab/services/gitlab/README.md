# GitLab Service

GitLabサーバーの実行環境を管理します。基本設定は [プロジェクトのREADME](../../README.md) を参照してください。

## ディレクトリ構造
### データ永続化
- `config/` - GitLab設定ファイル
- `data/` - リポジトリ、データベース等
- `logs/` - アプリケーションログ
- `backups/` - バックアップデータ

### Webhook設定
自動ラベル付けエージェント用のWebhook設定:
1. 設定 > Webhooks に移動
2. URLに `http://agents:8000/webhook` を設定
3. Secret Token を `.env` の `WEBHOOK_SECRET` と同じ値に設定
4. Issue events を有効化

詳細な設定は [エージェントのドキュメント](../../agents/README.md) を参照してください。