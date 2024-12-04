<div align="center">

![CloudFront Infrastructure for OpenWebUI](assets/header.svg)

</div>

EC2上で動作するOpenWebUI用のCloudFrontディストリビューションを設定するTerraformモジュールです。

## 🚀 機能

- CloudFrontディストリビューションの作成（*.cloudfront.netドメインを使用）
- WAFv2の設定
- 既存のセキュリティグループとの連携
- CloudFrontからEC2（OpenWebUI）へのアクセス設定

## 📋 前提条件

- AWS CLI がインストールされていること
- Terraform がインストールされていること
- 既存のEC2インスタンスとセキュリティグループが存在すること

## 📁 ファイル構成

```
cloudfront-infrastructure/
├── main.tf           # メインの設定とプロバイダー
├── cloudfront.tf     # CloudFrontディストリビューション設定
├── waf.tf           # WAF設定
├── variables.tf     # 変数定義
├── outputs.tf       # 出力定義
└── terraform.tfvars # 環境固有の変数
```

## 🛠️ セットアップ手順

1. `terraform.tfvars` を環境に合わせて編集:

```hcl
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-xxxxxxxx"
public_subnet_id   = "subnet-xxxxxxxx"
security_group_id  = "sg-xxxxxxxx"
project_name       = "amts-open-webui"
origin_domain      = "ec2-xx-xx-xx-xx.compute-1.amazonaws.com"
```

2. Terraformの初期化:
```bash
terraform init
```

3. 設定内容の確認:
```bash
terraform plan
```

4. インフラストラクチャの作成:
```bash
terraform apply
```

## ⚙️ 主な設定内容

### 🌐 CloudFront設定
- HTTPSへのリダイレクト有効
- OpenWebUIポート(8282)への転送
- デフォルトのCloudFrontドメイン使用

### 🛡️ WAF設定
- デフォルトですべてのアクセスを許可
- 基本的な保護を有効化

### 🔒 セキュリティ設定
- 既存のセキュリティグループを使用
- CloudFrontからEC2へのアクセスルールを自動追加

## 📤 出力値

- `cloudfront_domain_name`: CloudFrontのドメイン名（*.cloudfront.net）
- `cloudfront_distribution_id`: CloudFrontディストリビューションのID
- `cloudfront_arn`: CloudFrontディストリビューションのARN

## 🧹 環境の削除

```bash
terraform destroy
```

## 📝 注意事項

- このモジュールは既存のEC2インスタンスとセキュリティグループを前提としています
- CloudFrontのデフォルトドメインを使用するため、カスタムドメインの設定は含まれていません
- デフォルトでは全てのIPからのアクセスを許可しています

## 🔍 セキュリティグループIDの確認方法

AWS Management ConsoleでセキュリティグループIDを確認する手順：

1. EC2ダッシュボードを開く
2. 左側のメニューから「セキュリティグループ」を選択
3. 使用するセキュリティグループを見つけ、IDをコピー
4. `terraform.tfvars`の`security_group_id`に貼り付け

## ❓ トラブルシューティング

1. CloudFrontにアクセスできない場合：
   - セキュリティグループのルールを確認
   - OpenWebUIが8282ポートで正しく動作していることを確認

2. WAF関連の問題：
   - AWS ConsoleでWAFルールを確認
   - CloudFrontディストリビューションとWAFの連携を確認
