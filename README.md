<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">エンタープライズグレードのプライベートAIプラットフォーム (v1.19.0)</h2>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

>[!NOTE]
>AMATERASUは[MOA](https://github.com/Sunwood-ai-labs/MOA)の後継プロジェクトです。各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行し、Terraformで簡単にデプロイできるように進化させました。

## 🚀 プロジェクト概要

AMATERASUは、エンタープライズグレードのプライベートAIプラットフォームです。AWS BedrockとGoogle Vertex AIをベースに構築されており、セキュアでスケーラブルな環境でLLMを活用したアプリケーションを開発・運用できます。GitLabとの統合により、バージョン管理、CI/CDパイプライン、プロジェクト管理を効率化します。  v1.19.0では、Terraformによるインフラ構成管理の柔軟性と保守性が大幅に向上しました。具体的には、Terraform変数の追加、出力の追加、モジュール化、既存リソースのインポートスクリプト作成などを行いました。また、WAFの設定追加、ECSの設定追加、スケジューリング機能の追加など、セキュリティと運用性の向上に重点を置いたアップデートが含まれています。さらに、Dockerイメージの最適化、UIの改良、エラーハンドリングの強化なども行っています。


このリポジトリは、複数のAI関連プロジェクトを管理するための「呪文書（Spellbook）」として構成されています。各プロジェクトは、特定のAIサービスや機能をデプロイ・管理するための独立したフォルダとして構造化されています。

## ✨ 主な機能

### セキュアな基盤
- AWS BedrockとGoogle Vertex AIベースの安全なLLM基盤
- 完全クローズド環境での運用
- エンタープライズグレードのセキュリティ

### マイクロサービスアーキテクチャ
- 独立したサービスコンポーネント
- コンテナベースのデプロイメント
- 柔軟なスケーリング

### Infrastructure as Code
- Terraformによる完全自動化されたデプロイ
- 環境ごとの設定管理
- バージョン管理された構成

### GitLab統合
- バージョン管理、CI/CDパイプライン、プロジェクト管理機能の向上
- セルフホスト型GitLabインスタンスの統合
- LLMを用いたマージリクエスト分析
- GitLab Webhookを用いた自動ラベル付け

### プロジェクト探索機能
- Terraformプロジェクトの自動検出と`terraform.tfvars`ファイルの生成
- `amaterasu`コマンドラインツールによる簡素化された設定

## 🏗️ システムアーキテクチャ

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "Application Layer"
            subgraph "EC2-based Services"
                OW["Open WebUI<br/>チャットインターフェース"]
                LL["LiteLLM Proxy<br/>APIプロキシ"]
                LF["Langfuse<br/>モニタリング"]
                GL["GitLab<br/>バージョン管理"]
                CD["Coder<br/>クラウド開発環境"]
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>プロンプト生成支援"]
                ECS["ECS Fargate Cluster"]
            end
        end
        
        subgraph "Infrastructure Layer"
            CF["CloudFront"]
            WAF["WAF"]
            R53["Route 53"]
        end
        
        subgraph "AWS Services"
            Bedrock["AWS Bedrock<br/>LLMサービス"]
            IAM["IAM<br/>認証・認可"]
        end
        
        OW --> CF
        LL --> CF
        LF --> CF
        GL --> CF
        CD --> CF
        PP --> ECS
        
        CF --> WAF
        WAF --> R53
        
        EC2 --> Bedrock
        ECS --> Bedrock
        EC2 --> IAM
        ECS --> IAM
    end
```

## 📦 コンポーネント構成

### 1. Open WebUI (フロントエンド)
- チャットベースのユーザーインターフェース
- レスポンシブデザイン
- プロンプトテンプレート管理
    - [詳細はこちら](./spellbook/open-webui/README.md)

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- Google Vertex AIモデルへのアクセス
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


## 🆕 最新情報

### AMATERASU v1.19.0 (最新のリリース)

- 🎉 **Terraform変数の追加**: AWSリージョン、プロジェクト名、VPC設定、EC2インスタンス設定、アプリケーション設定、WAF設定などを柔軟に設定可能になりました。
- 🎉 **Terraform出力の追加**: CloudFront, ECS, セキュリティグループに関する情報を取得可能になりました。
- 🎉 **WAF(Web Application Firewall)の設定追加**: CloudFrontを保護するWAF Web ACLを作成し、IPホワイトリストによるアクセス制限を設定しました。
- 🎉 **セキュリティグループの設定追加**: ECSタスクとALB間の通信を許可するセキュリティグループを作成しました。
- 🎉 **アプリケーションのスケジューリング設定の追加**: Auto Scaling Targetを使用して、ECSサービスのDesiredCountを調整し、平日朝8時(JST)に起動、平日夜10時(JST)に停止するスケジュールを設定しました。
- 🎉 **IAM(Identity and Access Management)の設定追加**: ECSインスタンスプロファイル、ECSタスクロール、ECS実行ロールを作成し、必要なポリシーをアタッチしました。
- 🎉 **ECS(Elastic Container Service)の設定追加**: ECSクラスタ、タスク定義、サービスを作成し、CloudWatch LogsとALBと連携するように設定しました。
- 🎉 **EC2インスタンス、AutoScalingの設定追加**: ECSタスクを実行するためのEC2インスタンスを起動する設定を追加し、Auto Scaling Groupを利用してインスタンス数を管理します。
- 🎉 **CloudFrontの設定追加**: ALBをオリジンとするCloudFront Distributionの設定を追加しました。
- 🎉 **ALB(Application Load Balancer)の設定追加**: ALB、リスナー、ターゲットグループ、セキュリティグループを作成し、ALBはHTTPトラフィックをECSサービスに転送するように構成されています。
- 🎉 **アニメーション付きヘッダー画像の追加**: アプリケーションのヘッダーとしてアニメーション付きSVG画像を追加しました。
- 🎉 **UIの改良とエラーハンドリングの強化**: Streamlitを使用して、ユーザーフレンドリーなインターフェースを作成し、エラーハンドリングを強化しました。
- 🎉 **既存AWSリソースのTerraform stateへのインポートスクリプト作成**: 既存のAWSリソースをTerraform stateにインポートするスクリプトを作成しました。
- 🎉 **AWS ECSへのデプロイスクリプト作成**: AWS ECSクラスタとサービスにDockerイメージをデプロイするスクリプトを作成しました。
- 🎉 **Dockerイメージの最適化とヘルスチェックの追加**: Python 3.11-slimイメージをベースとしてイメージサイズを削減し、ヘルスチェックコマンドを追加しました。
- 🚀 **Terraform構成のモジュール化と変数化**: 全体構成をモジュール化し、各モジュールの変数を定義しました。
- 🚀 **READMEファイルの更新**: アプリケーションの概要、機能、環境構築方法、使用方法、デバッグ情報、AWS ECS Fargateへのデプロイ手順などを詳細に記述しました。
- 🚀 **docker-compose.ymlの修正とヘルスチェックの設定**: docker-compose.ymlの設定を修正し、ポートマッピングとヘルスチェックを正しく設定しました。
- 🚀 **CoderイメージのPython, Node.jsインストールとコードサーバー設定の改善**:  Python3とpip, Node.jsとnpmをインストールし、Python3をデフォルトのPythonとして設定しました。
- 🚀 **依存関係の更新と追加**: Streamlit、OpenAI、requestsライブラリを最新バージョンに更新し、dnspythonライブラリを追加しました。
- 🐛 **docker-compose.yml のポート修正**: ClickHouseのポート9000をコメントアウトしました。
- ⚠️ **ALB関連のリソースの削除**: グローバルアクセラレータとALBを用いたロードバランシング構成から、CloudFrontを利用した構成へ移行しました。


## 🔧 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。  `amaterasu`コマンドラインツールの使用方法については、`spellbook/amaterasu-tool-ui/README.md`を参照ください。


## 📦 インストール手順

1. リポジトリをクローンします。
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```
2. 各プロジェクトのREADMEに記載されている手順に従って、依存関係をインストールし、アプリケーションをデプロイします。
3. `terraform.tfvars`ファイルに必要な設定を入力します。  `amaterasu` ツールを利用して自動生成することもできます。


## 📦 依存関係

このリポジトリのルートディレクトリには、共通の依存関係を定義する`requirements.txt`ファイルがあります。
```bash
pip install -r requirements.txt
```

```plaintext
aira
sourcesage
```

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👏 謝辞

iris-s-coonとMakiへの貢献に感謝します。