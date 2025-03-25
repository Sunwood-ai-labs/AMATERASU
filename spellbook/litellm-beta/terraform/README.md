# 🚀 LiteLLM-Beta Terraform インフラストラクチャ

## 📌 概要

このTerraformコードは、LiteLLM-Betaのインフラストラクチャをセットアップします。パブリックおよび内部アクセス用の2つの環境を構築し、それぞれに適切な証明書とロードバランサーを設定します。

## 🏗️ インフラストラクチャ構成

- **VPC & サブネット**
  - パブリックサブネット x 2
  - セキュリティグループ

- **ロードバランサー（ALB）**
  - パブリック用ALB
  - 内部用ALB

- **証明書管理**
  - パブリックドメイン: AWS ACM証明書（DNS検証）
  - 内部ドメイン: 自己署名証明書

- **Route53**
  - パブリックホストゾーン
  - プライベートホストゾーン

## 🔒 証明書管理について

### パブリックドメイン証明書
- AWS ACM証明書を使用
- Route53でのDNS検証による自動検証
- 有効期間は自動更新

### 内部ドメイン証明書（自己署名）
- `.internal`ドメイン用に自己署名証明書を使用
- DNS検証が不要で即時発行可能
- 有効期間: 1年
- セキュアな内部通信を確保

## 🛠️ デプロイ方法

1. 環境変数の設定
```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="ap-northeast-1"
```

2. terraform.tfvarsの設定
```hcl
# 必要な値を設定
aws_region         = "ap-northeast-1"
domain             = "your-domain.com"
domain_internal    = "your-domain.internal"
...
```

3. Terraformの実行
```bash
cd main-infrastructure
terraform init
terraform plan
terraform apply
```

## 🌐 アクセス方法

デプロイ完了後、以下のURLでアクセス可能：

- パブリックアクセス: `https://litellm-beta.sunwood-ai-labs.com`
- 内部アクセス: `https://litellm-beta.sunwood-ai-labs.internal`

## 📊 出力値

| 出力名 | 説明 |
|--------|------|
| instance_id | EC2インスタンスID |
| instance_private_ip | プライベートIPアドレス |
| instance_public_dns | パブリックDNS名 |
| instance_public_ip | パブリックIPアドレス |
| internal_url | 内部アクセス用URL |
| public_url | パブリックアクセス用URL |
| security_group_id | セキュリティグループID |
| vpc_id | VPC ID |

## ⚠️ 注意事項

1. 内部ドメイン用の自己署名証明書は1年で期限切れとなります
2. 証明書の更新は手動で行う必要があります
3. ブラウザでアクセスする際は、自己署名証明書の警告が表示される場合があります
