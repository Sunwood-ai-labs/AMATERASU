<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
<h1 align="center">🌄 AMATERASU v0.3.0 🌄</h1>
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases">
    <img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/AMATERASU?style=social">
  </a>
</p>

<h2 align="center">
  ～ AWS上のLLMプラットフォームを自動構築 ～
</h2>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

>[!NOTE]
>AMATERASUは[MOA](https://github.com/Sunwood-ai-labs/MOA)の後継プロジェクトです。各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行し、Terraformで簡単にデプロイできるように進化させました。

## 🚀 プロジェクト概要

AMATERASUは、AWS上にLLM（大規模言語モデル）プラットフォームを構築するための自動化ツールです。MOAの機能を踏襲しながら、各サービスを独立したEC2インスタンスで運用することで、より柔軟なスケーリングと管理を実現します。

主な特徴:
- Terraformを使用した簡単なEC2インスタンス管理
- 各サービスごとに独立したEC2インスタンスとDocker Compose環境
- サービス単位でのスケーリングと運用が可能
- セキュアな通信とアクセス制御

## ✨ 主な機能

- TerraformによるAWSインフラの自動構築
- Docker Composeによる各サービスのコンテナ化と管理
- 複数のLLMモデルとの連携（OpenAI, Anthropic, Geminiなど）
- Langfuseによるモデル管理と課金機能


## 🔧 使用方法

このREADMEに記載されているインストール手順と使用方法に従って、AMATERASUをセットアップしてください。


## 📦 インストール手順

1. リポジトリのクローン:
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

2. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集して必要な認証情報を設定  (LITELLM_MASTER_KEY、LITELLM_SALT_KEY、OPENAI_API_KEY、ANTHROPIC_API_KEY、GEMINI_API_KEY、GEMINI_API_KEY_IRISなど)
```

3. Terraformの初期化と実行:
```bash
cd spellbook/open-webui/terraform
terraform init
terraform plan
terraform apply
```


## SSH

```bash
ssh -i "C:\Users\makim\.ssh\AMATERASU-terraform-keypair-tokyo-PEM.pem" ubuntu@i-062f3dd7388a5da8a
```

## 🆕 最新情報

### v0.3.0 の更新内容

- README.mdの更新: SourceSageとClaude.aiの利用について明記し、重要な情報を強調しました。
- 複数のClaudeモデル定義の追加: Langfuseで利用可能なClaudeモデルを拡張しました。(`claude-3.5-haiku-20241022`, `claude-3.5-haiku-latest`, `claude-3.5-sonnet-20240620`, `claude-3.5-sonnet-20241022`, `claude-3.5-sonnet-latest`, `claude-3-haiku-20240307`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`)
- LLaMAモデル連携のための環境変数設定の追加: 様々なLLaMAモデルプロバイダーとの連携を容易にしました。(`LITELLM_MASTER_KEY`、`LITELLM_SALT_KEY`、`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GEMINI_API_KEY`、`GEMINI_API_KEY_IRIS`)
- README.mdへのSSH接続情報の追加とインフラストラクチャ説明の更新: EC2インスタンスへのSSH接続方法と、v0.2.0でのアーキテクチャ刷新に関する説明を追加しました。
- 英語READMEの更新
- docker-compose.ymlのボリュームマウント修正
- ロギングライブラリの変更: `logging`モジュールから`loguru`モジュールに変更しました。


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 👏 謝辞

iris-s-coonとMakiに貢献への謝辞を述べます。

## 🤝 コントリビューション

コントリビューションを歓迎します！以下の手順で参加できます：

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📧 サポート

ご質問やフィードバックがありましたら、以下までお気軽にご連絡ください：
- Issue作成: [GitHub Issues](https://github.com/Sunwood-ai-labs/AMATERASU/issues)
- メール: support@sunwoodai.com

AMATERASUで、より柔軟で強力なAIインフラストラクチャを構築しましょう！ ✨