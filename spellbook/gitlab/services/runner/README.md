# GitLab Runner

CI/CDパイプラインの実行環境を管理します。

## 設定
- `config/` - Runner設定ファイル
  - `config.toml` - 主要な設定ファイル

## Runner登録
1. GitLabの設定からRunner登録トークンを取得
2. `.env` の `RUNNER_REGISTRATION_TOKEN` に設定
3. Runner自動登録の詳細は [GitLabのドキュメント](../gitlab/README.md) を参照

## 注意事項
- Docker executorを使用
- コンテナ内でCI/CDジョブを安全に実行