# モジュラー LLM Reviewer

GitLabのマージリクエストを自動的にレビューし、フィードバックを提供するモジュラー構造のツールです。
各モジュールは独立して実行可能で、デバッグや開発が容易になっています。

## プロジェクト構造

```plaintext
llm_reviewer/
├── src/
│   ├── gitlab_fetcher.py   # GitLabからMRデータを取得
│   ├── llm_analyzer.py     # LLMによる分析と結果保存
│   └── gitlab_commenter.py # GitLabへのコメント投稿
├── prompts/
│   └── review_prompt.txt   # LLM用のプロンプトテンプレート
├── outputs/                # 分析結果の保存ディレクトリ
├── main.py                 # メインスクリプト
└── README.md              # このファイル
```

## セットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. 環境変数の設定:
`.env`ファイルを作成し、以下の内容を設定：
```plaintext
# GitLab設定
GITLAB_URL=http://gitlab.example.com
GITLAB_TOKEN=your_gitlab_token_here

# OpenAI/LiteLLM設定
API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=your_api_key_here
```

## 利用可能なLLMモデル

レビューには以下のモデルを使用できます：
- `gpt-4` (デフォルト)
- `gpt-3.5-turbo`
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`
- `anthropic/claude-3-opus-20240229`
- `anthropic/claude-3-sonnet-20240229`
- `bedrock/anthropic.claude-3-sonnet-20240229`
- `bedrock/anthropic.claude-3-haiku-20240307`

## モジュール単体での実行方法

### 1. GitLab Fetcher

マージリクエストの情報を取得して表示します：

```bash
# MRの詳細を取得
python -m src.gitlab_fetcher --project-id <プロジェクトID> --mr-iid <MR番号>
```

### 2. LLM Analyzer
取得したMRをLLMで分析し、結果を保存します：

```bash
# LLM分析を実行（デフォルト設定）
python -m src.llm_analyzer --project-id <プロジェクトID> --mr-iid <MR番号> --output-dir outputs

# カスタムモデルと設定を使用
python -m src.llm_analyzer \
    --project-id <プロジェクトID> \
    --mr-iid <MR番号> \
    --model claude-3-sonnet-20240229 \
    --temperature 0.7 \
    --max-tokens 4000
```

### 3. GitLab Commenter
保存された分析結果をGitLabにコメントとして投稿します：

```bash
# 分析結果をコメントとして投稿
python -m src.gitlab_commenter --project-id <プロジェクトID> --mr-iid <MR番号> --analysis-file outputs/analysis_*.json
```

## パイプライン全体の実行

すべてのステップを一度に実行する場合：

```bash
# デフォルト設定（GPT-4）での実行
python main.py --project-id <プロジェクトID> --mr-iid <MR番号>

# Claude-3 Sonnetを使用
python main.py --project-id <プロジェクトID> --mr-iid <MR番号> \
    --model claude-3-sonnet-20240229

# カスタム設定での実行（より創造的な分析）
python main.py --project-id <プロジェクトID> --mr-iid <MR番号> \
    --model gpt-4 \
    --temperature 0.7 \
    --max-tokens 4000

# コメント投稿をスキップする場合
python main.py --project-id <プロジェクトID> --mr-iid <MR番号> --skip-comment

# 出力ディレクトリを指定する場合
python main.py --project-id <プロジェクトID> --mr-iid <MR番号> --output-dir custom_outputs
```

### オプション一覧
- `--project-id`: GitLabプロジェクトID（必須）
- `--mr-iid`: マージリクエスト番号（必須）
- `--model`: 使用するLLMモデル（デフォルト: gpt-4）
- `--temperature`: モデルの温度パラメータ（0.0-1.0、デフォルト: 0.3）
  - 低い値: より一貫性のある、保守的なレビュー
  - 高い値: より創造的で多様なフィードバック
- `--max-tokens`: レスポンスの最大トークン数（デフォルト: 2000）
- `--output-dir`: 分析結果の保存ディレクトリ（デフォルト: outputs）
- `--skip-comment`: GitLabへのコメント投稿をスキップ

## デバッグとトラブルシューティング

### 各モジュールの出力確認
1. GitLab Fetcher:
   - MRの詳細情報とdiffが正しく取得できているか確認
   - ネットワークエラーやトークンの問題を検出

2. LLM Analyzer:
   - `outputs/`ディレクトリに分析結果のJSONファイルが保存される
   - ファイル名形式: `analysis_<プロジェクトID>_<MR番号>_<タイムスタンプ>.json`
   - LLMのレスポンスや評価基準を確認可能
   - モデルや温度パラメータの影響を確認

3. GitLab Commenter:
   - 分析結果のフォーマットが正しいか確認
   - コメントの投稿権限やAPI接続を確認

### ログ出力
各モジュールは`loguru`を使用してログを出力します：
- 情報ログ: 処理の進行状況
- エラーログ: 問題発生時の詳細情報
- デバッグログ: 詳細なデバッグ情報

## 開発ガイド

### 新機能の追加
1. 適切なモジュールを選択または新規作成
2. モジュール単体でのテストを実装
3. `main.py`に統合
4. READMEの更新

### コードスタイル
- Type hintsの使用
- Docstringsの記述
- エラー処理の実装
- ログ出力の追加

### プロンプトのカスタマイズ
`prompts/review_prompt.txt`を編集することで、レビューの観点や評価基準を調整できます。

### モデルの追加
新しいLLMモデルを追加する場合は、以下の手順で行います：
1. `main.py`の`get_available_models()`に新しいモデルを追加
2. 必要に応じて`llm_analyzer.py`のリクエスト処理を調整
3. READMEのモデルリストを更新
