<div align="center">

![CloudFront Infrastructure Module](../../assets/header.svg)

</div>

# AWS CloudFront Infrastructure Module

このTerraformモジュールは、CloudFrontディストリビューションを作成し、以下の機能を提供します：

- CloudFrontディストリビューションの作成（カスタムドメイン対応）
- WAFv2によるIPホワイトリスト制御
- Route53でのDNSレコード自動設定
- ACM証明書の自動作成と検証

## 📋 使用方法

```hcl
module "cloudfront" {
  source = "../../modules/cloudfront"

  providers = {
    aws           = aws
    aws_virginia = aws.virginia
  }

  project_name      = "your-project"
  aws_region        = "ap-northeast-1"
  origin_domain     = "your-ec2-domain.compute.amazonaws.com"
  domain            = "example.com"
  subdomain         = "app"
  whitelist_csv_path = "${path.module}/whitelist-waf.csv"
}
```

## 🔧 要件

- Terraform 0.12以上
- AWS Provider ~> 4.0
- Route53で管理されているドメイン
- CSVファイルでのIPホワイトリスト定義

## ⚙️ 入力変数

| 名前 | 説明 | タイプ | デフォルト値 | 必須 |
|------|-------------|------|---------|:--------:|
| project_name | プロジェクト名 | `string` | - | はい |
| aws_region | AWSリージョン | `string` | `"ap-northeast-1"` | いいえ |
| origin_domain | オリジンサーバーのドメイン名 | `string` | - | はい |
| domain | メインドメイン名 | `string` | - | はい |
| subdomain | サブドメイン名 | `string` | - | はい |
| whitelist_csv_path | ホワイトリストCSVファイルのパス | `string` | - | はい |
| providers | AWSプロバイダー設定 | `object` | - | はい |

## 📤 出力値

| 名前 | 説明 |
|------|-------------|
| cloudfront_domain_name | CloudFrontのドメイン名 (*.cloudfront.net) |
| cloudfront_distribution_id | CloudFrontディストリビューションのID |
| cloudfront_arn | CloudFrontディストリビューションのARN |
| cloudfront_url | CloudFrontのURL |
| subdomain_url | サブドメインのURL |
| waf_web_acl_id | WAF Web ACLのID |
| waf_web_acl_arn | WAF Web ACLのARN |
| certificate_arn | ACM証明書のARN |

## 📁 WAFホワイトリストの設定

whitelist-waf.csvファイルは以下の形式で作成してください：

```csv
ip,description
192.168.1.1/32,Office Network
10.0.0.1/32,Home Network
203.0.113.0/24,Client Network
```

## 🚀 使用例

完全な使用例は `examples/complete` ディレクトリを参照してください。

## 📝 注意事項

1. CloudFrontのデプロイには15-30分程度かかることがあります
2. DNSの伝播には最大72時間かかる可能性があります
3. SSL証明書の検証には数分から数十分かかることがあります
4. WAFのIPホワイトリストは定期的なメンテナンスが必要です

## 🔍 トラブルシューティング

1. CloudFrontにアクセスできない場合：
   - ホワイトリストにIPが正しく登録されているか確認
   - Route53のDNSレコードが正しく作成されているか確認
   - ACM証明書の検証が完了しているか確認

2. SSL証明書の検証に失敗する場合：
   - Route53のゾーン設定が正しいか確認
   - ドメインの所有権が正しく確認できているか確認

3. オリジンサーバーにアクセスできない場合：
   - EC2インスタンスが起動しているか確認
   - オリジンドメインが正しく設定されているか確認
