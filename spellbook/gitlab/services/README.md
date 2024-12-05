<div align="center">

![](../assets/services_header.svg)

# Services

Docker ベースのサービス群を管理するディレクトリです。

</div>

## サービス構成
- [GitLab](gitlab/README.md) - メインのGitLabサーバー
- [Runner](runner/README.md) - CI/CD実行環境

## 設定管理
- 基本設定は各サービスのディレクトリを参照
- 共通設定は `../docker-compose.yml` で管理
- 環境変数は `../.env` で設定（テンプレート: `../.env.example`）