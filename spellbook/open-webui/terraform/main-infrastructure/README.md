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
- セキュリティグループ管理
  - 複数のセキュリティグループの統合管理
  - 用途別のセキュリティグループ：
    1. デフォルトセキュリティグループ（基本的なインバウンド/アウトバウンドルール）
    2. CloudFrontセキュリティグループ（CDNからのアクセス制御）
    3. VPC内部通信用セキュリティグループ（内部サービス間の通信）
    4. ホワイトリストセキュリティグループ（特定IPからのアクセス許可）
  - 優先順位とルールの結合
    - すべてのグループのルールが統合されて適用
    - より制限の厳しいルールが優先
    - 明示的な許可が必要（デフォルトでは拒否）
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
```hcl
# terraform.tfvarsの設定例
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0fde6326ce23fcb11"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-07ccf2ba130266f91"
public_subnet_2_id = "subnet-035f1861e57534990"

# セキュリティグループの設定
security_group_ids = [
  "sg-07f88719c48f3c042",  # デフォルトセキュリティグループ
  "sg-03e35cd397ab91b2d",  # CloudFrontセキュリティグループ
  "sg-0097221f0bf87d747",  # VPC内部通信用セキュリティグループ
  "sg-0a7a8064abc5c1aee"   # ホワイトリストセキュリティグループ
]

# その他の設定
project_name       = "amts-open-webui"
instance_type     = "t3.medium"
key_name          = "your-key-pair-name"
```

2. セキュリティグループの確認
```bash
# 各セキュリティグループのルールを確認
aws ec2 describe-security-groups --group-ids sg-07f88719c48f3c042
aws ec2 describe-security-groups --group-ids sg-03e35cd397ab91b2d
aws ec2 describe-security-groups --group-ids sg-0097221f0bf87d747
aws ec2 describe-security-groups --group-ids sg-0a7a8064abc5c1aee
```

3. モジュールの初期化とデプロイ
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

### セキュリティグループについて
- 複数のセキュリティグループを使用する際の注意点：
  - 各セキュリティグループのルールは加算的に適用されます
  - 特定のルールが複数のグループで重複する場合は、最も制限の緩いルールが適用されます
  - インバウンドルールとアウトバウンドルールは独立して評価されます

- よくある問題と解決方法：
  1. EC2インスタンスへの接続ができない
     ```bash
     # セキュリティグループのルールを確認
     aws ec2 describe-security-group-rules --filters Name="group-id",Values="sg-07f88719c48f3c042"
     # 必要なポートが開放されているか確認
     ```
  2. 特定のサービスからのアクセスが拒否される
     ```bash
     # CloudFrontセキュリティグループのルールを確認
     aws ec2 describe-security-group-rules --filters Name="group-id",Values="sg-03e35cd397ab91b2d"
     # CloudFrontのIPレンジが許可されているか確認
     ```
  3. VPC内部での通信が機能しない
     ```bash
     # VPC内部通信用セキュリティグループを確認
     aws ec2 describe-security-group-rules --filters Name="group-id",Values="sg-0097221f0bf87d747"
     # VPC CIDRからのトラフィックが許可されているか確認
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
