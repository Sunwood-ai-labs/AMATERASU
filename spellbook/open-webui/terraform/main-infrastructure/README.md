<div align="center">

![Open WebUI Infrastructure](../../assets/header.svg)

# Main Infrastructure Module

Core infrastructure components for Open WebUI deployment

</div>

## 🎯 概要

Open WebUIのコアインフラストラクチャを管理するTerraformモジュールです。EC2、VPC、ALB、IAMなどの主要なAWSリソースを統合的に管理します。

## 📦 モジュール構成

### Common Module (`modules/common/`)
- プロジェクト全体で使用される変数と設定の定義
- タグ管理とリソース命名規則

### Compute Module (`modules/compute/`)
- EC2インスタンス管理
- 自動起動/停止スケジュール
- ボリューム設定
- ネットワークインターフェース設定
  - プライベートIPの自動割り当て
  - プライベートDNSホスト名の自動生成

### IAM Module (`modules/iam/`)
- サービスロールとポリシー
- インスタンスプロファイル
- 最小権限の原則に基づく設定

### Networking Module (`modules/networking/`)
- VPC設定とサブネット管理
- ALBとターゲットグループ
- Route53 DNS管理
  - パブリックDNSレコード管理
  - プライベートホストゾーン設定
    - VPC内部向けDNSレコード自動作成
    - サブドメイン: `<subdomain>.sunwood-ai-labs-internal.com`
    - EC2インスタンスのプライベートDNSホスト名を使用したCNAMEレコード
      - 形式: `ip-10-0-1-98.ap-northeast-1.compute.internal`
      - インスタンス再起動時のIP変更に自動追従
      - AWSの組み込みDNS機能を活用した堅牢な名前解決

## 🛠️ デプロイメント手順

1. 環境変数の設定
```bash
# terraform.tfvarsを環境に合わせて編集
```

2. モジュールの初期化とデプロイ
```bash
terraform init
terraform plan
terraform apply
```

3. プライベートDNSの確認
```bash
# terraform出力でDNSレコード情報を確認
terraform output private_dns_info

# VPC内のEC2インスタンスからの疎通確認
curl http://<subdomain>.sunwood-ai-labs-internal.com
```

詳細な設定手順と変数については[親ディレクトリのREADME](../README.md)を参照してください。

## 📝 出力値

主要な出力値：

- VPC/サブネット情報
  - VPC ID
  - CIDRブロック
  - パブリックサブネットID
- EC2インスタンス詳細
  - インスタンスID
  - パブリックIP/DNS
  - プライベートIP
  - プライベートDNSホスト名
- ALB設定
  - ターゲットグループ情報
  - リスナー設定
- DNS情報
  - パブリックDNS設定
    - ACM証明書ARN
  - プライベートDNS設定
    - ホストゾーンID
    - 作成されたDNSレコード情報
      - ドメイン名: `<subdomain>.sunwood-ai-labs-internal.com`
      - レコードタイプ: CNAME
      - TTL: 300秒
      - ターゲット: EC2インスタンスのプライベートDNSホスト名

## ⚠️ トラブルシューティング

### プライベートDNS解決について
- EC2インスタンスのプライベートIPは再起動時に変更される可能性がありますが、プライベートDNSホスト名は自動的に新しいIPを指すため、アプリケーションの可用性は維持されます
- VPC内のDNS解決はAWSによって自動的に処理され、プライベートDNSホスト名は常に正しいIPアドレスを返します
- CNAMEレコードを使用することで、IPアドレスの変更に対して堅牢な設計となっています

### 内部通信について
- VPC内部では全てのトラフィックが許可されており、セキュリティグループで特別な設定は不要です
- 現在、アプリケーションはHTTPでのアクセスのみをサポートしています
  ```bash
  # 正常なアクセス例（HTTP）
  curl http://<subdomain>.sunwood-ai-labs-internal.com
  
  # HTTPSは現在サポートされていません
  # アプリケーションでHTTPSを有効にする場合は、追加の設定が必要です
  ```

### 接続確認スクリプト
プライベートDNSの動作確認には、提供されている接続確認スクリプトを使用できます：
```bash
python3 scripts/connectivity_health_check.py
```
このスクリプトは以下を確認します：
- DNS名前解決
- PING疎通確認
- HTTP接続確認
- レスポンスの内容確認

その他の問題については[CloudFront Infrastructure](../cloudfront-infrastructure/README.md)も併せて参照してください。
