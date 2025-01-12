<div align="center">

![](assets/header.svg)

# GitLab Project

このプロジェクトは、Docker ComposeベースのGitLabインスタンスと、カスタムエージェントを提供します。

</div>

## プロジェクト構造

```plaintext
C:\Prj\AMATERASU\spellbook\gitlab\
├─ agents/                      # エージェント関連のコード
├─ services/                    # Dockerサービス関連
│  ├─ gitlab/                  # GitLabサービス
│  └─ runner/                  # GitLab Runner
├─ docker-compose.yml          # Docker Compose設定
├─ .env.example                # 環境変数テンプレート
└─ terraform/                  # Terraform設定
```

## コンポーネント
- [エージェント](agents/README.md) - カスタムエージェントの実装とドキュメント
- [サービス](services/README.md) - GitLabおよび関連サービスの設定と管理

## クイックスタート

1. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集
```

2. GitLabの起動:
```bash
docker compose up -d
```

3. 初期パスワードの取得:
```bash
docker compose exec gitlab cat /etc/gitlab/initial_root_password
```

## 要件
- Docker 20.10以上
- Docker Compose v2.0以上
- システム要件：
  - CPU: 4コア
  - メモリ: 8GB以上
  - ストレージ: 50GB以上

## インフラストラクチャ構成

- CloudFront経由のアクセス制御
- WAFによるIPホワイトリスト管理
- SSL/TLS証明書の自動管理
- Route53によるDNS管理

## セキュリティ設定

- セキュリティグループ設定
- ネットワークアクセス制御
- HTTPS通信の強制
- WAFルールセットによる保護

詳細な設定手順については[Terraform Infrastructure](terraform/README.md)を参照してください。
