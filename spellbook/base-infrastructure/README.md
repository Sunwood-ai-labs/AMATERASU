<div align="center">

![Base Infrastructure](./assets/header.svg)

# ベースインフラストラクチャ

AMATERASUの基盤となるAWSインフラストラクチャ構成

</div>

## 🌟 概要

このモジュールは、AMATERASUプラットフォームの基盤となるAWSインフラストラクチャを提供します。VPC、サブネット、セキュリティグループ、Route53などの基本的なネットワークリソースを管理します。

## 📦 主要コンポーネント

### 🔒 セキュリティグループ構成

モジュール化された柔軟なセキュリティグループにより、きめ細かなアクセス制御を実現：

1. **デフォルトセキュリティグループ** (`default.tf`)
   - 基本的なセキュリティ設定のベース
   - 分割された各セキュリティグループからのトラフィックを許可
   - すべてのアウトバウンドトラフィックを許可

2. **ホワイトリストSG** (`whitelist_sg.tf`)
   - 特定のIPアドレスからのすべてのインバウンドトラフィックを許可
   - CSVファイル（`whitelist-base-sg.csv`）による柔軟なIP管理
   - 各IPエントリに対する説明付きの動的ルール生成

3. **CloudFront SG** (`cloudfront_sg.tf`)
   - CloudFrontエッジロケーションからのアクセスを制御
   - HTTP(80)およびHTTPS(443)ポートへのアクセスを許可
   - AWSマネージドプレフィックスリストを使用した効率的な管理

4. **VPC内部SG** (`vpc_internal_sg.tf`)
   - VPC内部の通信を包括的に制御
   - すべてのポートでVPC CIDR範囲（10.0.0.0/16）からの通信を許可
   - マイクロサービス間の安全な通信を確保

### 🌐 Route53 DNS設定

1. **パブリックホストゾーン**
   - メインドメイン: `sunwood-ai-labs.com`
   - パブリックアクセス用

2. **プライベートホストゾーン**
   - 内部ドメイン: `sunwood-ai-labs-internal.com`
   - VPC内部での名前解決
   - EC2インスタンス間の通信に使用

## 🛠️ セットアップ手順

1. 環境変数の設定
```bash
# terraform.tfvarsを編集
cp terraform.example.tfvars terraform.tfvars
```

2. 必要なCSVファイルの準備
```bash
# ホワイトリストIPの設定
cp whitelist-base-sg.example.csv whitelist-base-sg.csv
```

3. Terraformの実行
```bash
terraform init
terraform plan
terraform apply
```

## ⚙️ 設定パラメータ

主要な設定パラメータ（`terraform.tfvars`）：

```hcl
# プロジェクト設定
project_name = "amts-base-infrastructure"
environment  = "dev"

# ドメイン設定
domain_name = "sunwood-ai-labs.com"
domain_internal = "sunwood-ai-labs-internal.com"

# ネットワーク設定
vpc_cidr             = "10.0.0.0/16"
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
```

## 🔍 動作確認

1. セキュリティグループの確認
```bash
# デフォルトSGのルール確認
aws ec2 describe-security-group-rules --filter Name="group-id",Values="<default-sg-id>"
```

2. Route53レコードの確認
```bash
# プライベートホストゾーンのレコード一覧
aws route53 list-resource-record-sets --hosted-zone-id <private-zone-id>
```

## 📝 注意事項

1. セキュリティグループの更新
   - 既存の依存関係に注意
   - 更新前にバックアップを推奨

2. Route53設定の変更
   - DNSの伝播時間を考慮
   - 既存のレコードへの影響を確認

詳細な設定や追加のカスタマイズについては、各モジュールのREADMEを参照してください。
