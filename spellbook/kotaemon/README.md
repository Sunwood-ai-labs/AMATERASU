# Kotaemon Docker環境

このリポジトリは[Kotaemon](https://github.com/Cinnamon/kotaemon)のDocker環境を提供します。KotaemonはドキュメントとチャットするためのオープンソースのRAG UIツールです。

## 🚀 セットアップ

### 前提条件

- Docker
- Docker Compose

### 🛠️ インストール手順

1. リポジトリをクローン：
```bash
git clone <repository-url>
cd kotaemon
```

2. 環境設定：
- `.env`ファイルを編集し、必要な設定を行います
  - OpenAI APIキーなどの設定が必要な場合は、`.env`ファイルで設定してください

3. アプリケーションの起動：
```bash
docker compose up -d
```

4. ブラウザでアクセス：
- `http://localhost:7860` にアクセスしてください
- デフォルトのユーザー名とパスワードは両方とも `admin` です

## 📝 環境設定

### 主な設定ファイル

1. `docker-compose.yaml`
   - Dockerコンテナの設定
   - ポート設定やボリュームマウントの管理

2. `.env`
   - 環境変数の設定
   - APIキーや各種モデルの設定
   - サーバー設定の管理

### データの永続化

アプリケーションのデータは`./ktem_app_data`ディレクトリに保存されます。このディレクトリをバックアップすることで、設定やデータを保持できます。

## 🔧 カスタマイズ

- 各種設定は`.env`ファイルで管理されています
- さらに詳細な設定は[Kotaemonの公式ドキュメント](https://cinnamon.github.io/kotaemon/)を参照してください

## 🔒 セキュリティ

- デフォルトの認証情報（admin/admin）は必ず変更してください
- APIキーは適切に管理し、公開リポジトリにコミットしないよう注意してください

## 📚 参考リンク

- [Kotaemon公式リポジトリ](https://github.com/Cinnamon/kotaemon)
- [ドキュメント](https://cinnamon.github.io/kotaemon/)
