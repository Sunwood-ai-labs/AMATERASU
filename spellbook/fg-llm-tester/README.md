# 🚀 LLM Proxy Connection Tester

シンプルなStreamlitベースのLLMプロキシ疎通確認用アプリケーション

## 📋 機能

- LiteLLM Proxyとの疎通確認
- UIでの各種パラメータ制御
  - Base URL設定
  - API Key設定
  - モデル名設定
  - トークン数制御
  - Temperature制御
- デバッグ情報の表示
  - パブリックIP
  - ローカルIP
  - ホスト名
  - レスポンス詳細

## 🔧 環境構築

### ローカル開発環境

```bash
# 1. リポジトリのクローン
git clone [repository-url]
cd llm-proxy-connection-tester

# 2. 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 依存パッケージのインストール
pip install -r requirements.txt

# 4. アプリケーションの起動
streamlit run app.py
```

### Dockerでの実行

```bash
# Docker Composeでビルド＆起動
docker-compose up --build

# バックグラウンドで実行する場合
docker-compose up -d --build
```

## 💻 使用方法

1. アプリケーションにアクセス: `http://localhost:8501`
2. サイドバーで必要な設定を行う
   - LiteLLM Proxy URLの設定
   - API Keyの設定
   - モデル名の指定
   - 各種パラメータの調整
3. プロンプトを入力して送信
4. 結果の確認とデバッグ情報の参照

## 🐳 コンテナ構成

- ベースイメージ: `python:3.11-slim`
- 公開ポート: 8501
- ヘルスチェック設定済み

## 🔍 デバッグ情報

アプリケーションは以下のデバッグ情報を表示します：
- パブリックIPアドレス
- ローカルIPアドレス
- ホスト名
- APIレスポンスの詳細（JSONフォーマット）

## 🚀 AWS ECS Fargateへのデプロイ

1. ECRリポジトリの作成
```bash
aws ecr create-repository --repository-name llm-proxy-connection-tester
```

2. イメージのビルドとプッシュ
```bash
# ECRログイン
aws ecr get-login-password | docker login --username AWS --password-stdin [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com

# イメージのビルドとタグ付け
docker build -t llm-proxy-connection-tester .
docker tag llm-proxy-connection-tester:latest [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/llm-proxy-connection-tester:latest

# ECRへのプッシュ
docker push [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/llm-proxy-connection-tester:latest
```

3. ECS Fargateタスク定義とサービスの作成
- Terraformまたはマネジメントコンソールを使用してECS Fargateの設定を行う
- 必要なIAMロールとセキュリティグループを設定
- コンテナのポートマッピング（8501）を設定
- ヘルスチェックのパスを`/_stcore/health`に設定

## 📝 注意事項

- デバッグ目的のアプリケーションのため、本番環境での使用は推奨しません
- API KeyなどのSecretは適切に管理してください
- パブリックIPの取得にはexternal APIを使用しています
