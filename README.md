<div align="center">

![Supabase Infrastructure](assets/header.svg)

<h2 align="center">エンタープライズグレードのプライベートAIプラットフォーム (🚀 AMATERASU v1.22.0)</h2>

Terraformを使用したSupabaseのセルフホスティング環境の構築とCloudFrontによるCDN配信の自動化

</div>

## 🎯 概要

このプロジェクトは、AWS上でSupabaseをセルフホスティングするための完全な Infrastructure as Code (IaC) ソリューションを提供します。TerraformとDockerを使用して、安全で拡張性の高いインフラストラクチャを自動的に構築します。

## 🏗️ アーキテクチャ

プロジェクトは以下の主要コンポーネントで構成されています：

- 📦 **Supabase Self-hosting**
  - PostgreSQLデータベース
  - Auth, Storage, Edge Functionsなどのサービス
  - 管理用ダッシュボード

- 🌐 **CDN配信**
  - CloudFrontによる高速なコンテンツ配信
  - WAFによるセキュリティ制御
  - カスタムドメイン対応

## 🚀 クイックスタート

### 前提条件

- AWS CLI設定済み
- Terraform v0.12以上
- Docker & Docker Compose

### セットアップ手順

![](docs/flow.svg)

- AMATERASU Base Infrastructureは再利用可能な基盤コンポーネントを提供し、コストと管理オーバーヘッドを削減
- 異なる目的のセキュリティグループ（Default、CloudFront、VPC Internal、Whitelist）で多層的なセキュリティを実現
- AMATERASU EC2 ModuleはEC2インスタンス上でDockerコンテナを実行
- AMATERASU EE ModuleはECSクラスターを使用し、開発環境からECRにデプロイして運用
- 両モジュールはCloudFrontとWAFによるIPホワイトリストで保護され、同じベースインフラストラクチャを共有
- インフラ全体はTerraformでモジュール化された設計によって管理され、同じセキュリティグループとネットワーク設定を活用

## 📦 コンポーネント構成

### 1. Open WebUI (フロントエンド)
- チャットベースのユーザーインターフェース
- レスポンシブデザイン
- プロンプトテンプレート管理
    - [詳細はこちら](./spellbook/open-webui/README.md)

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- Google Vertex AIモデルへのアクセス
- OpenRouter API統合
- APIキー管理とレート制限
    - [詳細はこちら](./spellbook/litellm/README.md)

### 3. Langfuse (モニタリング)
- 使用状況の追跡
- コスト分析
- パフォーマンスモニタリング
    - [詳細はこちら](./spellbook/langfuse3/README.md)

### 4. GitLab (バージョン管理)
- セルフホストGitLabインスタンス
- プロジェクトとコード管理
- CIパイプラインとRunner設定
- バックアップと復元機能

### 5. FG-prompt-pandora (Fargate版サンプルアプリケーション)
- AWS Fargateでの自動スケーリング
- Claude-3.5-Sonnetを活用したプロンプト生成
- Streamlitベースの直感的UI
    - [詳細はこちら](./spellbook/fg-prompt-pandora/README.md)

### 6. Coder (クラウド開発環境)
- WebベースのIDE環境
- VS Code拡張機能のサポート
- AWSインフラストラクチャ上でのセキュアな開発
    - [詳細はこちら](./spellbook/Coder/README.md)

### 7. Dify (AIアプリケーション開発プラットフォーム)
- 様々なAIモデルを統合したアプリケーション開発プラットフォーム
- UI/APIベースの開発が可能
    - [詳細はこちら](./spellbook/dify/README.md)

### 8. Dify Beta (AIアプリケーション開発プラットフォーム)
- 新機能と実験的な機能を含むDifyのベータ版
- ベクトルデータベースとサンドボックス環境の高度な設定が可能
    - [詳細はこちら](./spellbook/dify-beta1/README.md)

### 9. Open WebUI Pipeline
- Open WebUIとの連携を強化するパイプライン機能
- 会話ターン制限やLangfuse連携などのフィルター処理が可能
    - [詳細はこちら](./spellbook/open-webui-pipeline/README.md)

### 10. Amaterasu Tool (Terraform 変数ジェネレーター)
-  コマンドラインツールで`terraform.tfvars`ファイルの生成を自動化
- spellbook の各プロジェクトを対象に設定値を生成
    - [詳細はこちら](./spellbook/amaterasu-tool-ui/README.md)

### 11. Kotaemon (ドキュメントとチャットRAG UIツール)
- ドキュメントとチャットするためのRAG UIツール
- Docker環境とTerraform設定を提供
- データ永続化とカスタマイズ可能な環境設定
- セキュアな認証システムを実装
    - [詳細はこちら](./spellbook/kotaemon/README.md)

### 12. Bolt DIY (AIチャットインターフェース)
- 最新のAIチャットインターフェース
- 複数のAIプロバイダー（OpenAI、Anthropic、Google等）をサポート
- Dockerコンテナ化された環境を提供
- CloudFrontインフラストラクチャの設定
    - [詳細はこちら](./spellbook/bolt-diy/README.md)

### 13.  LLMテスター(Gradio版)
- GradioベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-gr/README.md)

### 14. LLMテスター(Streamlit版)
- StreamlitベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-st/README.md)

### 15. Marp Editable UI (Markdown プレゼンテーション編集ツール)
- Markdown形式でプレゼンテーションを作成・編集できるWebアプリケーション
- Dockerコンテナ化された環境を提供
    - [詳細はこちら](./spellbook/ee-marp-editable-ui/README.md)

### 16. App Gallery Showcase (プロジェクト紹介Webアプリケーション)
- プロジェクトを視覚的に美しく紹介するWebアプリケーション
- Dockerコンテナ化された環境を提供
    - [詳細はこちら](./spellbook/app-gallery-showcase/README.md)


## 🔧 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。  `amaterasu`コマンドラインツールの使用方法については、`spellbook/amaterasu-tool-ui/README.md`を参照ください。


## 📦 インストール手順

1. リポジトリをクローンします。

![](docs/flow.svg)

- AMATERASU Base Infrastructureは再利用可能な基盤コンポーネントを提供し、コストと管理オーバーヘッドを削減
- 異なる目的のセキュリティグループ（Default、CloudFront、VPC Internal、Whitelist）で多層的なセキュリティを実現
- AMATERASU EC2 ModuleはEC2インスタンス上でDockerコンテナを実行
- AMATERASU EE ModuleはECSクラスターを使用し、開発環境からECRにデプロイして運用
- 両モジュールはCloudFrontとWAFによるIPホワイトリストで保護され、同じベースインフラストラクチャを共有
- インフラ全体はTerraformでモジュール化された設計によって管理され、同じセキュリティグループとネットワーク設定を活用

## 📦 コンポーネント構成

### 1. Open WebUI (フロントエンド)
- チャットベースのユーザーインターフェース
- レスポンシブデザイン
- プロンプトテンプレート管理
    - [詳細はこちら](./spellbook/open-webui/README.md)

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- Google Vertex AIモデルへのアクセス
- OpenRouter API統合
- APIキー管理とレート制限
    - [詳細はこちら](./spellbook/litellm/README.md)

### 3. Langfuse (モニタリング)
- 使用状況の追跡
- コスト分析
- パフォーマンスモニタリング
    - [詳細はこちら](./spellbook/langfuse3/README.md)

### 4. GitLab (バージョン管理)
- セルフホストGitLabインスタンス
- プロジェクトとコード管理
- CIパイプラインとRunner設定
- バックアップと復元機能

### 5. FG-prompt-pandora (Fargate版サンプルアプリケーション)
- AWS Fargateでの自動スケーリング
- Claude-3.5-Sonnetを活用したプロンプト生成
- Streamlitベースの直感的UI
    - [詳細はこちら](./spellbook/fg-prompt-pandora/README.md)

### 6. Coder (クラウド開発環境)
- WebベースのIDE環境
- VS Code拡張機能のサポート
- AWSインフラストラクチャ上でのセキュアな開発
    - [詳細はこちら](./spellbook/Coder/README.md)

### 7. Dify (AIアプリケーション開発プラットフォーム)
- 様々なAIモデルを統合したアプリケーション開発プラットフォーム
- UI/APIベースの開発が可能
    - [詳細はこちら](./spellbook/dify/README.md)

### 8. Dify Beta (AIアプリケーション開発プラットフォーム)
- 新機能と実験的な機能を含むDifyのベータ版
- ベクトルデータベースとサンドボックス環境の高度な設定が可能
    - [詳細はこちら](./spellbook/dify-beta1/README.md)

### 9. Open WebUI Pipeline
- Open WebUIとの連携を強化するパイプライン機能
- 会話ターン制限やLangfuse連携などのフィルター処理が可能
    - [詳細はこちら](./spellbook/open-webui-pipeline/README.md)

### 10. Amaterasu Tool (Terraform 変数ジェネレーター)
-  コマンドラインツールで`terraform.tfvars`ファイルの生成を自動化
- spellbook の各プロジェクトを対象に設定値を生成
- [詳細はこちら](./spellbook/amaterasu-tool-ui/README.md)

### 11. Kotaemon (ドキュメントとチャットRAG UIツール)
- ドキュメントとチャットするためのRAG UIツール
- Docker環境とTerraform設定を提供
- データ永続化とカスタマイズ可能な環境設定
- セキュアな認証システムを実装
    - [詳細はこちら](./spellbook/kotaemon/README.md)

### 12. Bolt DIY (AIチャットインターフェース)
- 最新のAIチャットインターフェース
- 複数のAIプロバイダー（OpenAI、Anthropic、Google等）をサポート
- Dockerコンテナ化された環境を提供
- CloudFrontインフラストラクチャの設定
    - [詳細はこちら](./spellbook/bolt-diy/README.md)

### 13.  LLMテスター(Gradio版)
- GradioベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-gr/README.md)

### 14. LLMテスター(Streamlit版)
- StreamlitベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-st/README.md)


## 🔧 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。  `amaterasu`コマンドラインツールの使用方法については、`spellbook/amaterasu-tool-ui/README.md`を参照ください。


## 📦 インストール手順

1. リポジトリをクローンします。

![](docs/flow.svg)

- AMATERASU Base Infrastructureは再利用可能な基盤コンポーネントを提供し、コストと管理オーバーヘッドを削減
- 異なる目的のセキュリティグループ（Default、CloudFront、VPC Internal、Whitelist）で多層的なセキュリティを実現
- AMATERASU EC2 ModuleはEC2インスタンス上でDockerコンテナを実行
- AMATERASU EE ModuleはECSクラスターを使用し、開発環境からECRにデプロイして運用
- 両モジュールはCloudFrontとWAFによるIPホワイトリストで保護され、同じベースインフラストラクチャを共有
- インフラ全体はTerraformでモジュール化された設計によって管理され、同じセキュリティグループとネットワーク設定を活用

## 📦 コンポーネント構成

### 1. Open WebUI (フロントエンド)
- チャットベースのユーザーインターフェース
- レスポンシブデザイン
- プロンプトテンプレート管理
    - [詳細はこちら](./spellbook/open-webui/README.md)

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- Google Vertex AIモデルへのアクセス
- OpenRouter API統合
- APIキー管理とレート制限
    - [詳細はこちら](./spellbook/litellm/README.md)

### 3. Langfuse (モニタリング)
- 使用状況の追跡
- コスト分析
- パフォーマンスモニタリング
    - [詳細はこちら](./spellbook/langfuse3/README.md)

### 4. GitLab (バージョン管理)
- セルフホストGitLabインスタンス
- プロジェクトとコード管理
- CIパイプラインとRunner設定
- バックアップと復元機能

### 5. FG-prompt-pandora (Fargate版サンプルアプリケーション)
- AWS Fargateでの自動スケーリング
- Claude-3.5-Sonnetを活用したプロンプト生成
- Streamlitベースの直感的UI
    - [詳細はこちら](./spellbook/fg-prompt-pandora/README.md)

### 6. Coder (クラウド開発環境)
- WebベースのIDE環境
- VS Code拡張機能のサポート
- AWSインフラストラクチャ上でのセキュアな開発
    - [詳細はこちら](./spellbook/Coder/README.md)

### 7. Dify (AIアプリケーション開発プラットフォーム)
- 様々なAIモデルを統合したアプリケーション開発プラットフォーム
- UI/APIベースの開発が可能
    - [詳細はこちら](./spellbook/dify/README.md)

### 8. Dify Beta (AIアプリケーション開発プラットフォーム)
- 新機能と実験的な機能を含むDifyのベータ版
- ベクトルデータベースとサンドボックス環境の高度な設定が可能
    - [詳細はこちら](./spellbook/dify-beta1/README.md)

### 9. Open WebUI Pipeline
- Open WebUIとの連携を強化するパイプライン機能
- 会話ターン制限やLangfuse連携などのフィルター処理が可能
    - [詳細はこちら](./spellbook/open-webui-pipeline/README.md)

### 10. Amaterasu Tool (Terraform 変数ジェネレーター)
-  コマンドラインツールで`terraform.tfvars`ファイルの生成を自動化
- spellbook の各プロジェクトを対象に設定値を生成
    - [詳細はこちら](./spellbook/amaterasu-tool-ui/README.md)

### 11. Kotaemon (ドキュメントとチャットRAG UIツール)
- ドキュメントとチャットするためのRAG UIツール
- Docker環境とTerraform設定を提供
- データ永続化とカスタマイズ可能な環境設定
- セキュアな認証システムを実装
    - [詳細はこちら](./spellbook/kotaemon/README.md)

### 12. Bolt DIY (AIチャットインターフェース)
- 最新のAIチャットインターフェース
- 複数のAIプロバイダー（OpenAI、Anthropic、Google等）をサポート
- Dockerコンテナ化された環境を提供
- CloudFrontインフラストラクチャの設定
    - [詳細はこちら](./spellbook/bolt-diy/README.md)

### 13.  LLMテスター(Gradio版)
- GradioベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-gr/README.md)

### 14. LLMテスター(Streamlit版)
- StreamlitベースのLLMプロキシ接続テスター
- 各種パラメータ設定とデバッグ情報表示
    - [詳細はこちら](./spellbook/ee-llm-tester-st/README.md)

### 15. Marp Editable UI (Markdown プレゼンテーション編集ツール)
- Markdown形式でプレゼンテーションを作成・編集できるWebアプリケーション
- Dockerコンテナ化された環境を提供
    - [詳細はこちら](./spellbook/ee-marp-editable-ui/README.md)

### 16. App Gallery Showcase (プロジェクト紹介Webアプリケーション)
- プロジェクトを視覚的に美しく紹介するWebアプリケーション
- Dockerコンテナ化された環境を提供
    - [詳細はこちら](./spellbook/app-gallery-showcase/README.md)


## 🔧 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。  `amaterasu`コマンドラインツールの使用方法については、`spellbook/amaterasu-tool-ui/README.md`を参照ください。


## 📦 インストール手順

1. リポジトリをクローンします。
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
