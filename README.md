<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
<h1 align="center">🌄 AMATERASU v0.2.0 🌄</h1>
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
>AMATERASUは[MOA](https://github.com/Sunwood-ai-labs/MOA)の後継プロジェクトです。各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行し、Terraformで簡単にデプロイできるように進化させました。

## 🚀 プロジェクト概要

AMATERASUは、AWS上にLLM（大規模言語モデル）プラットフォームを構築するための自動化ツールです。MOAの機能を踏襲しながら、各サービスを独立したEC2インスタンスで運用することで、より柔軟なスケーリングと管理を実現します。

主な特徴:
- Terraformを使用した簡単なEC2インスタンス管理
- 各サービスごとに独立したEC2インスタンスとDocker Compose環境
- サービス単位でのスケーリングと運用が可能
- セキュアな通信とアクセス制御

## ✨ 主な機能

- なし


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
# .envファイルを編集して必要な認証情報を設定
```

3. Terraformの初期化と実行:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```


## SSH

```bash
ssh -i "C:\Users\makim\.ssh\AMATERASU-terraform-keypair-tokyo-PEM.pem" ubuntu@i-062f3dd7388a5da8a
```

## 🆕 最新情報

v0.2.0では、アーキテクチャを刷新し、各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行するように変更しました。これにより、各サービスのスケーリングと運用が容易になり、柔軟性が向上しています。また、英語READMEの更新と、リリースノートの見栄えを向上させるための画像の追加を行いました。

アーキテクチャ刷新に伴い、READMEにアーキテクチャ図、システム要件、インストール手順、モジュール構成、デプロイ方法、運用コマンド例、各モジュールの詳細なディレクトリ構成、Docker Compose設定ファイル(docker-compose.yml)と環境変数ファイル(.env)の例、各モジュールへのSSH接続、Docker Composeによるサービス管理(起動、停止、ログ表示)を行うスクリプトが追加されました。セキュリティ強化のため、各EC2インスタンスは独立したセキュリティグループで保護され、サービス間通信は内部VPCネットワークで制御されるようになりました。


## 🌐 モジュール構成

各モジュールは独立したEC2インスタンス上でDocker Composeを使って実行されます：

### open-webui モジュール（EC2インスタンス）
```
📁 open-webui/
├── 📄 docker-compose.yml  # open-webuiとollamaの設定
├── 📄 .env               # 環境変数設定
└── 📁 config/            # 設定ファイル
```

設定例（docker-compose.yml）:
```yaml
version: '3'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ./data:/root/.ollama

  open-webui:
    image: open-webui/open-webui
    ports:
      - "3000:3000"
    environment:
      - OLLAMA_URL=http://ollama:11434
```

### litellm モジュール（EC2インスタンス）
```
📁 litellm/
├── 📄 docker-compose.yml  # litellmサービスの設定
├── 📄 .env               # API keyなどの環境変数
└── 📁 config/            # LLMの設定ファイル
```

### langfuse モジュール（EC2インスタンス）
```
📁 langfuse/
├── 📄 docker-compose.yml  # langfuseとDBの設定
├── 📄 .env               # 環境変数設定
└── 📁 data/              # PostgreSQLデータ
```

## 🔨 デプロイコマンド例

特定のモジュールのみデプロイ:
```bash
# open-webuiモジュールのみデプロイ
terraform apply -target=module.ec2_open_webui

# litellmモジュールのみデプロイ
terraform apply -target=module.ec2_litellm

# langfuseモジュールのみデプロイ
terraform apply -target=module.ec2_langfuse
```

## 💻 モジュール管理コマンド

各EC2インスタンスへの接続:
```bash
# SSH接続スクリプト
./scripts/connect.sh open-webui
./scripts/connect.sh litellm
./scripts/connect.sh langfuse
```

Docker Compose操作:
```bash
# 各インスタンス内で実行
cd /opt/amaterasu/[module-name]
docker-compose up -d      # サービス起動
docker-compose down      # サービス停止
docker-compose logs -f   # ログ表示
```

## 🔒 セキュリティ設定

- 各EC2インスタンスは独立したセキュリティグループで保護
- サービス間通信は内部VPCネットワークで制御
- 必要最小限のポートのみを公開
- IAMロールによる権限管理

## 📚 ディレクトリ構造

```plaintext
amaterasu/
├── terraform/          # Terraformコード
│   ├── modules/        # 各EC2インスタンスのモジュール
│   ├── main.tf        # メイン設定
│   └── variables.tf   # 変数定義
├── modules/           # 各サービスのDocker Compose設定
│   ├── open-webui/    # open-webui関連ファイル
│   ├── litellm/      # litellm関連ファイル
│   └── langfuse/     # langfuse関連ファイル
├── scripts/          # 運用スクリプト
└── docs/            # ドキュメント
```

## ⚠️ 重要な変更

- アーキテクチャが刷新されたため、以前のバージョンからのアップグレードには、手順に従って手動での移行が必要です。詳細については、アップグレード手順を参照してください。


## 📦 アップグレード手順

1. 既存の環境を停止してください。
2. このREADMEに記載されている手順に従って、新しいアーキテクチャで環境を構築してください。
3. データの移行が必要な場合は、適切な手順を実行してください。(具体的な手順は提供されていません。)


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 👏 謝辞

iris-s-coonとMakiに感謝します。

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
