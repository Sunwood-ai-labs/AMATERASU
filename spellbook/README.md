<div align="center">

![AMATERASU Spellbook](assets/header.svg)

# AMATERASU Spellbook

魔法のように Infrastructure as Code を実現する呪文集

</div>

## 🌟 概要

AMATERASUスペルブックは、さまざまなインフラストラクチャとアプリケーションの展開を自動化するための包括的な呪文（コード）コレクションです。

## 📚 スペル（プロジェクト）一覧

- [Open WebUI](./open-webui/README.md) - Ollama WebUIのインフラストラクチャ自動構築
  - CloudFrontとALBを利用した高可用性アーキテクチャ
  - セキュアなSSL/TLS通信
  - Dockerコンテナ化されたアプリケーション

## 🎯 特徴

- 完全自動化されたインフラストラクチャのデプロイメント
- セキュリティベストプラクティスの実装
- モジュール化された再利用可能なコード
- 包括的なドキュメント

## 🛠️ 前提条件

- AWS CLI
- Terraform
- Docker
- Docker Compose

## 🔮 使用方法

1. 必要なツールのインストール
```bash
# AWS CLIのインストール
# Terraformのインストール
# Dockerのインストール
```

2. リポジトリのクローン
```bash
git clone https://github.com/your-username/amaterasu-spellbook.git
cd amaterasu-spellbook
```

3. 目的のスペル（プロジェクト）ディレクトリに移動
```bash
cd <spell-directory>
```

4. スペルの詳細な使用方法は各プロジェクトのREADMEを参照

## ⚡ クイックスタート

最も一般的なスペルの使用例：

```bash
# Open WebUIのデプロイ
cd open-webui
# 環境変数の設定
cp .env.example .env
# インフラストラクチャのデプロイ
cd terraform/main-infrastructure
terraform init
terraform apply
```

## 🔒 セキュリティ

- すべてのスペルはAWSのセキュリティベストプラクティスに従っています
- SSL/TLS暗号化が標準で有効
- 最小権限の原則に基づくIAM設定
- セキュリティグループの適切な設定

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-spell`)
3. 変更をコミット (`git commit -m 'Add some amazing spell'`)
4. ブランチにプッシュ (`git push origin feature/amazing-spell`)
5. Pull Requestを作成

## 📞 サポート

質問や問題がありましたら、GitHubのIssueセクションをご利用ください。