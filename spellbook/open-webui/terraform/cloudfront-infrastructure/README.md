<div align="center">

![CloudFront Infrastructure for OpenWebUI](assets/header.svg)

</div>

EC2上で動作するOpenWebUI用のCloudFrontディストリビューションを設定するTerraformモジュールです。WAFによるIPホワイトリスト制御とカスタムドメインの設定が可能です。

## 🚀 機能

- CloudFrontディストリビューションの作成（カスタムドメイン対応）
- WAFv2によるIPホワイトリスト制御
- Route53でのDNSレコード自動設定
- ACM証明書の自動作成と検証
- CloudFrontからEC2（OpenWebUI）へのアクセス設定

## 📋 前提条件

- AWS CLIがインストールされていること
- Terraformがインストールされていること（バージョン0.12以上）
- 既存のEC2インスタンスが稼働していること
- Route53で管理されているドメインが存在すること

## 📁 ファイル構成

```
cloudfront-infrastructure/
├── acm.tf                    # ACM証明書の作成と検証設定
├── cloudfront.tf             # CloudFrontディストリビューション設定
├── main.tf                   # Terraform初期化とプロバイダー設定
├── outputs.tf                # 出力値の定義
├── route53.tf                # Route53 DNSレコード設定
├── variables.tf              # 変数定義
├── waf.tf                    # WAF設定とIPホワイトリスト制御
├── whitelist-waf.csv         # WAFホワイトリストIP定義
└── terraform.tfvars          # 環境固有の変数設定
```

## ⚙️ 主な設定内容

### 🌐 CloudFront設定 ([cloudfront.tf](cloudfront.tf))
- HTTPSへのリダイレクト有効
- カスタムドメインの使用
- オリジンへのHTTPプロトコル転送
- カスタムキャッシュ設定

### 🛡️ WAF設定 ([waf.tf](waf.tf))
- IPホワイトリストによるアクセス制御（[whitelist-waf.csv](whitelist-waf.csv)で定義）
- デフォルトでアクセスをブロック
- ホワイトリストに登録されたIPのみアクセス可能

### 🔒 DNS設定 ([route53.tf](route53.tf))
- Route53での自動DNSレコード作成
- CloudFrontへのエイリアスレコード設定

### 📜 SSL/TLS証明書 ([acm.tf](acm.tf))
- ACM証明書の自動作成
- DNS検証の自動化
- 証明書の自動更新設定

### ⚡ 変数設定 ([variables.tf](variables.tf))
- 環境設定用の変数定義（[terraform.tfvars](terraform.tfvars)で値を設定）
- ネットワーク設定
- ドメイン設定

### 📊 出力設定 ([outputs.tf](outputs.tf))
- CloudFront関連の情報出力
- URL情報の出力

## 🛠️ セットアップ手順

1. [terraform.tfvars](terraform.tfvars)を環境に合わせて編集します:

```hcl
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-xxxxxxxx"
public_subnet_id   = "subnet-xxxxxxxx"
security_group_id  = "sg-xxxxxxxx"
project_name       = "your-project-name"
origin_domain      = "your-ec2-domain.compute.amazonaws.com"
domain             = "your-domain.com"
subdomain          = "your-subdomain"
```

2. [whitelist-waf.csv](whitelist-waf.csv)にアクセスを許可するIPアドレスを設定:

```csv
ip,description
192.168.1.1/32,Office
10.0.0.1/32,Home
```

3. Terraformの初期化:
```bash
terraform init
```

4. 設定内容の確認:
```bash
terraform plan
```

5. インフラストラクチャの作成:
```bash
terraform apply
```

## 📤 出力値

- `cloudfront_domain_name`: CloudFrontのドメイン名（*.cloudfront.net）
- `cloudfront_distribution_id`: CloudFrontディストリビューションのID
- `cloudfront_arn`: CloudFrontディストリビューションのARN
- `cloudfront_url`: CloudFrontのURL（https://）
- `subdomain_url`: カスタムドメインのURL（https://）

## 🧹 環境の削除

```bash
terraform destroy
```

## 📝 注意事項

- CloudFrontのデプロイには15-30分程度かかることがあります
- DNSの伝播には最大72時間かかる可能性があります
- [whitelist-waf.csv](whitelist-waf.csv)のIPホワイトリストは定期的なメンテナンスが必要です
- SSL証明書の検証には数分から数十分かかることがあります

## 🔍 トラブルシューティング

1. CloudFrontにアクセスできない場合：
   - [whitelist-waf.csv](whitelist-waf.csv)のホワイトリストにIPが正しく登録されているか確認
   - Route53のDNSレコードが正しく作成されているか確認
   - ACM証明書の検証が完了しているか確認

2. SSL証明書の検証に失敗する場合：
   - Route53のゾーン設定が正しいか確認
   - ドメインの所有権が正しく確認できているか確認

3. オリジンサーバーにアクセスできない場合：
   - EC2インスタンスが起動しているか確認
   - セキュリティグループのインバウンドルールを確認
   - [terraform.tfvars](terraform.tfvars)のオリジンドメインが正しく設定されているか確認
