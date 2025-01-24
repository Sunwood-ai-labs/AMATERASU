# 📚 使用方法ガイド

## 🎮 アプリケーションの起動

### 基本的な起動方法

```bash
# PYTHONPATHを設定して起動
PYTHONPATH=/path/to/amaterasu-tool-ui python amaterasu_tool_ui/app.py
```

デフォルトでは http://localhost:7860 でアクセス可能です。

### 設定可能なオプション

- `server_name`: リッスンするインターフェース（デフォルト: "0.0.0.0"）
- `server_port`: ポート番号（デフォルト: 7860）
- `share`: 公開リンクの生成（デフォルト: False）

## 🖥️ インターフェースの使用方法

アプリケーションは3つの主要な機能を提供します：

### 1. 🔄 Generate TFVars

terraform.tfvarsファイルを生成するためのインターフェースです。

1. プロジェクトの選択
   - 表示されたプロジェクト一覧から対象を選択
   - 「全て選択」または「全て解除」ボタンで一括操作可能

2. 共通設定の入力
   - プラットフォーム正式名称（例: amaterasu）
   - プラットフォーム略式名称（例: amts）
   - 共通ドメイン名

3. プロジェクトごとの設定
   - サブドメイン
   - プロジェクト名
   - インスタンスタイプ
   - AMI ID
   - キーペア名

4. 生成の実行
   - 「生成開始」ボタンをクリック
   - 進捗状況が表示されます

### 2. 🧹 Cache Manager

Terraformのキャッシュファイルを管理します。

1. クリーニング対象の選択
   - プロジェクト一覧から対象を選択

2. キャッシュの削除
   - 「削除実行」ボタンで処理を開始
   - 以下のファイルが削除されます：
     - `.terraform/`
     - `terraform.tfstate`
     - `terraform.tfstate.backup`
     - `.terraform.lock.hcl`

### 3. 🌐 CloudFront TFVars

CloudFront用のterraform.tfvarsファイルを生成します。

1. 前提条件
   - まず「Generate TFVars」でmain-infrastructure用の設定を生成
   - CloudFrontインフラストラクチャを持つプロジェクトのみ表示

2. 設定項目
   - オリジンドメインの設定
   - カスタムドメインの設定
   - セキュリティ設定

3. 生成の実行
   - 「生成開始」ボタンで処理を開始
   - main-infrastructure/output.jsonが存在しない場合はデフォルト値を使用

## ⚠️ 注意事項

- 設定変更前には必ずバックアップを作成してください
- キャッシュ削除の操作は取り消せません
- output.jsonが存在しない場合はデフォルト値が使用されます

## 🔍 よくある問題

### プロジェクトが表示されない

- ディレクトリ構造が正しいか確認してください
- main-infrastructureディレクトリが存在することを確認
- CloudFrontの場合は、cloudfront-infrastructureディレクトリも必要

### 設定ファイルの生成に失敗する

- 書き込み権限があることを確認
- ディレクトリパスが正しいか確認
- 必要な情報がすべて入力されているか確認
