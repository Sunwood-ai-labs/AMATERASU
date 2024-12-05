<div align="center">

![](../assets/agents_header.svg)

# Agents

このディレクトリには、GitLabと連携する自動化エージェントが含まれています。

</div>

## エージェント一覧

### LLMベース自動ラベル付けエージェント
- `auto_labeling.py` - GitLab issueの自動ラベル付け
  - Webhook経由で Issue 作成イベントをトリガーとして動作
  - LLMを使用して issue の内容を分析し、適切なラベルを自動付与
  - 詳細な設定は [services/gitlab/README.md](../services/gitlab/README.md) のWebhook設定を参照

### LLMレビューエージェント
- `llm_reviewer/` - GitLab マージリクエストの自動レビュー
  - LLMを使用したコードレビューを実施
  - 詳細は [llm_reviewer/README.md](llm_reviewer/README.md) を参照

## セットアップ

### 環境変数の設定
`.env.example`をコピーして`.env`を作成し、必要な環境変数を設定してください：

```plaintext
# GitLab設定
GITLAB_URL=http://gitlab.example.com
GITLAB_TOKEN=your_gitlab_token_here

# OpenAI/LiteLLM設定
API_BASE=https://amaterasu-litellm-dev.example.com
OPENAI_API_KEY=your_api_key_here

# Webhook設定（auto_labeling.py用）
WEBHOOK_SECRET=your_webhook_secret_here
PORT=8000
HOST=0.0.0.0
ENV=development
```

### 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 開発ガイド
新しいエージェントを追加する場合は、以下の点に注意してください：

1. このディレクトリに新しいPythonファイルまたはディレクトリを配置
2. 必要な依存関係があれば`requirements.txt`に追加
3. READMEにエージェントの概要と詳細ドキュメントへのリンクを記載
4. 環境変数が必要な場合は`.env.example`に追加

## 依存ライブラリ
詳細は `requirements.txt` を参照してください。
