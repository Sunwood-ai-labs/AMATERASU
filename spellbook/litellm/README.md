<div align="center">

![AMATERASU LiteLLM](./assets/header.svg)

多様なLLMプロバイダーを統一的に扱うためのインフラストラクチャ管理ツールです。[LiteLLM](https://github.com/BerriAI/litellm)をベースに、AWS Bedrock、Anthropic Claude、OpenAI、Google Geminiなど、様々なLLMサービスを一元管理できます。

</div>

## 🌟 主な機能

- **統一されたAPI**: 異なるLLMプロバイダーに対して一貫したインターフェースを提供
- **マルチプロバイダー対応**: 
  - AWS Bedrock (Claude 3系)
  - Anthropic Direct API
  - OpenAI
  - Google Gemini
  - その他多数のプロバイダーをサポート
- **インフラ管理**: 
  - Docker Composeによる簡単なデプロイ
  - Prometheusによるメトリクス監視
  - PostgreSQLによるデータ永続化

## 🚀 クイックスタート

### 環境設定

1. 必要な環境変数を`.env`ファイルに設定：
```bash
# main config
LITELLM_MASTER_KEY="sk-1234"
LITELLM_SALT_KEY="sk-1234"

# provider
OPENAI_API_KEY="sk-xxxxx"
ANTHROPIC_API_KEY=sk-ant-xxxx
GEMINI_API_KEY=AIxxxx
```

2. `config.yaml`でモデル設定を行う：
```yaml
model_list:
  - model_name: bedrock/claude-3-5-sonnet
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
      aws_region_name: us-east-1

  - model_name: Anthropic/claude-3-5-sonnet-20240620
    litellm_params: 
      model: claude-3-5-sonnet-20240620 
      api_key: "os.environ/ANTHROPIC_API_KEY" 
```

### 🐳 Dockerを使用した起動

```bash
docker-compose up -d
```

## 🧪 テストツール

スクリプトディレクトリには、LiteLLMプロキシサーバーの機能をテストするための各種スクリプトが用意されています。

詳細については、[スクリプトディレクトリのREADME](./script/README.md)を参照してください。

## 🏗️ インフラストラクチャ

### Terraform構成

- `terraform/main-infrastructure/`: メインのインフラ定義
  - AWS VPC、EC2、ALB等のリソース管理
  - Route 53によるドメイン管理
  - 自動化されたデプロイメントプロセス

### モニタリング

Prometheusを使用したメトリクス収集：

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'litellm'
    static_configs:
      - targets: ['litellm:4000']
```

## 📂 プロジェクト構造

```plaintext
├─ script/                  # ユーティリティスクリプト
├─ terraform/              # インフラ定義
│  ├─ main-infrastructure/
├─ assets/                # プロジェクトアセット
├─ config.yaml            # LiteLLM設定
├─ docker-compose.yml     # Docker構成
├─ prometheus.yml         # モニタリング設定
```

## 🤝 コントリビューション

プロジェクトへの貢献は大歓迎です！以下の方法で参加できます：

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
