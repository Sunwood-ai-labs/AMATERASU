<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">エンタープライズグレードのプライベートAIプラットフォーム (v1.6.1)</h2>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

>[!NOTE]
>AMATERASUは[MOA](https://github.com/Sunwood-ai-labs/MOA)の後継プロジェクトです。各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行し、Terraformで簡単にデプロイできるように進化させました。

## 🚀 プロジェクト概要

AMATERASUは、エンタープライズグレードのプライベートAIプラットフォームです。AWS Bedrockをベースに構築されており、セキュアでスケーラブルな環境でLLMを活用したアプリケーションを開発・運用できます。GitLabとの統合により、バージョン管理、CI/CDパイプライン、プロジェクト管理を効率化します。  AMATERASU v1.6.1では、Bedrock Novaモデルのテストスクリプトを追加し、その他いくつかの機能強化と修正を行いました。


## ✨ 主な機能

### セキュアな基盤
- AWS Bedrockベースの安全なLLM基盤
- 完全クローズド環境での運用
- エンタープライズグレードのセキュリティ

### マイクロサービスアーキテクチャ
- 独立したサービスコンポーネント
- コンテナベースのデプロイメント
- 柔軟なスケーリング

### Infrastructure as Code
- Terraformによる完全自動化されたデプロイ
- 環境ごとの設定管理
- バージョン管理された構成

### GitLab統合
- バージョン管理、CI/CDパイプライン、プロジェクト管理機能の向上
- セルフホスト型GitLabインスタンスの統合
- LLMを用いたマージリクエスト分析機能
- GitLab Webhookを用いた自動ラベル付けサービス


## 🏗️ システムアーキテクチャ

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "Application Layer"
            subgraph "EC2-based Services"
                OW["Open WebUI<br/>チャットインターフェース"]
                LL["LiteLLM Proxy<br/>APIプロキシ"]
                LF["Langfuse<br/>モニタリング"]
                GL["GitLab<br/>バージョン管理"]
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>プロンプト生成支援"]
                ECS["ECS Fargate Cluster"]
            end
        end
        
        subgraph "Infrastructure Layer<br>(AMATERASU Architecture)"
            ALB["Application Load Balancer"]
            EC2["EC2 Instances"]
            SG["Security Groups"]
            R53["Route 53"]
            ACM["ACM Certificates"]
            ECR["Elastic Container Registry"]
        end
        
        subgraph "AWS Services"
            Bedrock["AWS Bedrock<br/>LLMサービス"]
            IAM["IAM<br/>認証・認可"]
        end
        
        OW --> ALB
        LL --> ALB
        LF --> ALB
        GL --> ALB
        PP --> ECS
        ECS --> ALB
        ALB --> EC2
        ALB --> ECS
        EC2 --> SG
        ECS --> SG
        R53 --> ALB
        ACM --> ALB
        ECR --> ECS
        EC2 --> Bedrock
        ECS --> Bedrock
        EC2 --> IAM
        ECS --> IAM
    end

    Users["Enterprise Users"] --> R53
```

## 📦 コンポーネント構成

### 1. Open WebUI (フロントエンド)
- チャットベースのユーザーインターフェース
- レスポンシブデザイン
- プロンプトテンプレート管理

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- APIキー管理
- レート制限と負荷分散

### 3. Langfuse (モニタリング)
- 使用状況の追跡
- コスト分析
- パフォーマンスモニタリング

### 4. GitLab (バージョン管理)
- セルフホストGitLabインスタンス
- プロジェクト管理とコード管理
- CIパイプラインとGitLab Runner
- バックアップと復元機能
- LDAP/Active Directory統合
- カスタマイズ可能な認証とアクセス制御

### 5. FG-prompt-pandora (Fargate版サンプルアプリケーション)
- AWS Fargateでの自動スケーリング
- Claude-3.5-Sonnetを活用したプロンプト生成
- Streamlitベースの直感的UI
- シンプルなDockerイメージによる容易なデプロイ
- AMATERASU環境への統合サンプル


## 🔧 デプロイメントガイド

### 前提条件
- AWS アカウント
- Terraform >= 0.12
- Docker & Docker Compose
- AWS CLI configured

### セットアップ手順

1. リポジトリのクローン
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

2. 環境変数の設定
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. インフラのデプロイ (spellbookディレクトリ内の各サービスのインフラを個別にデプロイする必要があります。)
```bash
cd spellbook/base-infrastructure
terraform init && terraform apply

cd ../open-webui/terraform/main-infrastructure
terraform init && terraform apply

cd ../../litellm/terraform/main-infrastructure
terraform init && terraform apply

cd ../../langfuse/terraform/main-infrastructure
terraform init && terraform apply

cd ../../gitlab/terraform/main-infrastructure
terraform init && terraform apply

cd ../../FG-prompt-pandora/terraform
terraform init && terraform apply
```

4. サービスの起動 (spellbookディレクトリ内の各サービスを個別に起動する必要があります。)

```bash
# Langfuse
cd ../../../langfuse
docker-compose up -d

# LiteLLM
cd ../litellm
docker-compose up -d

# Open WebUI
cd ../open-webui
docker-compose up -d

# GitLab
cd ../gitlab
docker-compose up -d

# FG-prompt-pandora
cd ../FG-prompt-pandora
docker-compose up -d
```

### GitLabのセットアップ

1. 環境設定ファイルの作成：
```bash
cd spellbook/gitlab
cp .env.example .env
```

2. 環境変数の設定：  `.env` ファイルを編集して、`GITLAB_HOME`, `GITLAB_HOSTNAME`, `GITLAB_ROOT_PASSWORD` などの必要な環境変数を設定してください。

3. GitLabの起動：
```bash
docker-compose up -d
```

4. バックアップの設定（オプション）：バックアップディレクトリを作成し、`docker-compose exec gitlab gitlab-backup create` コマンドでバックアップを実行してください。


## 📈 運用管理

### モニタリング
- Prometheusによるメトリクス収集
- Langfuseでの使用状況分析
- CloudWatchによるリソースモニタリング

### スケジューリング
- 平日8:00-22:00の自動起動/停止
- 需要に応じた手動スケーリング
- バッチジョブのスケジューリング

### セキュリティ
- IPホワイトリスト制御
- TLS/SSL暗号化
- IAMロールベースのアクセス制御

## 💡 ユースケース

### プロンプトエンジニアリング支援
- タスク記述からの最適なプロンプト生成
- 既存プロンプトの改善提案
- プロンプトテンプレートの管理と共有
- チーム全体でのプロンプト品質の標準化

### LLMアプリケーション開発
- APIプロキシを介した安全なモデルアクセス
- 使用状況の可視化と分析
- コスト管理とリソース最適化
- セキュアな開発環境の提供


## 🆕 最新情報

### AMATERASU v1.6.1 (最新のリリース)

- 🎉 **Bedrock Novaモデルテストスクリプト追加**:  Bedrock Novaモデル(`bedrock/nova-micro`, `bedrock/nova-lite`, `bedrock/nova-pro`)のテストを自動化するスクリプトを追加しました。応答時間、応答内容、トークン使用量などをログ出力します。`text2art`と`loguru`ライブラリを使用しています。
- 🎉 **LiteLLM設定ファイルの拡張とAWS設定の追加**: `.env.example`ファイルにOpenAI、Anthropic、Google Gemini、AWSのAPIキーと認証情報の項目を追加しました。AWS設定にはアクセスキーID、シークレットアクセスキー、デフォルトリージョン（東京）の設定が含まれています。
- 🚀 **不要なログ設定削除**: `loguru`ライブラリの不要なログ設定を削除し、簡素化しました。
- ⚠️  **`config.yaml`ファイル内のBedrockモデルの指定方法変更と地域指定の修正**: `bedrock/us.amazon.nova-micro-v1:0` のような表記を `bedrock/amazon.nova-micro-v1:0` に変更し、Bedrockモデルのリージョン指定を修正しました。


### AMATERASU v1.6.0 (以前のリリース)

- 🎉 **LLMを用いたマージリクエスト分析機能実装**: OpenAI APIとの連携、プロンプトエンジニアリングによるレビュー結果の生成、分析結果のJSONファイルへの保存、データクラスを用いたデータ構造の定義、エラーハンドリングとログ出力、環境変数による設定などを含みます。
    - コード品質、セキュリティ、テスト、アーキテクチャの観点からのレビューと改善提案を出力します。
- 🎉 **GitLab Webhookを用いた自動ラベル付けサービス実装**: FastAPIを用いたWebhookサーバー、GitLab APIとOpenAI API(LiteLLM Proxy経由)との連携、LLMによるIssueタイトルと説明からのラベル自動付与、ngrokを用いた開発環境での公開URL設定(開発環境のみ)、ヘルスチェックエンドポイントとログ出力機能の追加、Webhookトークンによる認証、エラー処理と例外ハンドリング、既存ラベルの保持と新規ラベルの追加、ログ出力機能強化、環境変数による設定管理、型ヒントとDocstringsによるコード品質向上など。
    - Issueイベントをトリガーとして、LLMを使用して自動的に適切なラベルを付与します。
- 🚀 **GitLabサービスのREADME.md作成**: ディレクトリ構造、Webhook設定について記述しました。
- 🚀 **GitLab RunnerのREADME.md作成**: 設定、Runner登録方法、注意事項について記述しました。
- 🚀 **servicesディレクトリのREADME.md作成**: サービス構成、設定管理について記述しました。
- 🚀 **services_header.svgのデザイン変更**: アニメーション追加、グラデーションの色変更、影の追加を行いました。
- 🚀 **agents_header.svgのデザイン変更**: アニメーション追加、グラデーションの色変更、影の追加を行いました。
- 🚀 **GitLab設定ディレクトリ作成**: 設定ディレクトリを作成しました。
- 🚀 **GitLabデータディレクトリ作成**: データディレクトリを作成しました。
- 🚀 **GitLabログディレクトリ作成**: ログディレクトリを作成しました。
- 🚀 **GitLabバックアップディレクトリ作成**: バックアップディレクトリを作成しました。
- 🚀 **GitLab Runner設定ディレクトリ作成**: 設定ディレクトリを作成しました。
- 🚀 **依存ライブラリの更新**: FastAPI, uvicorn, python-gitlab, openai, python-dotenv, pydantic, pyngrok, loguru, rich, argparseのバージョン更新を行いました。


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご参照ください。

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📞 サポート

不明点やフィードバックがありましたら、以下までお気軽にご連絡ください：
- GitHub Issues: [Issues](https://github.com/Sunwood-ai-labs/AMATERASU/issues)
- Email: support@sunwoodai.com

## 👏 謝辞

Maki、iris-s-coon の貢献に感謝します。

---

AMATERASUで、エンタープライズグレードのAIプラットフォームを構築しましょう。✨