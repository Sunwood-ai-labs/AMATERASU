<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">エンタープライズグレードのプライベートAIプラットフォーム (v1.9.0)</h2>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

>[!NOTE]
>AMATERASUは[MOA](https://github.com/Sunwood-ai-labs/MOA)の後継プロジェクトです。各AIサービスを独立したEC2インスタンス上でDocker Composeを用いて実行し、Terraformで簡単にデプロイできるように進化させました。

## 🚀 プロジェクト概要

AMATERASUは、エンタープライズグレードのプライベートAIプラットフォームです。AWS BedrockとGoogle Vertex AIをベースに構築されており、セキュアでスケーラブルな環境でLLMを活用したアプリケーションを開発・運用できます。GitLabとの統合により、バージョン管理、CI/CDパイプライン、プロジェクト管理を効率化します。

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
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>プロンプト生成支援"]
                ECS["ECS Fargate Cluster"]
            end
        end
        
        subgraph "Infrastructure Layer"
            ALB["Application Load Balancer"]
            CF["CloudFront"]
            WAF["WAF"]
            R53["Route 53"]
            ACM["ACM証明書"]
        end
        
        subgraph "AWS Services"
            Bedrock["AWS Bedrock<br/>LLMサービス"]
            IAM["IAM<br/>認証・認可"]
        end
        
        OW --> ALB
        LL --> ALB
        LF --> ALB
        GL --> ALB
        PP --> ECS
        
        ALB --> CF
        CF --> WAF
        WAF --> R53
        R53 --> ACM
        
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

### 2. LiteLLM (APIプロキシ)
- Claude-3系列モデルへの統一的なアクセス
- Google Vertex AIモデルへのアクセス
- APIキー管理とレート制限

### 3. Langfuse (モニタリング)
- 使用状況の追跡
- コスト分析
- パフォーマンスモニタリング

### 4. GitLab (バージョン管理)
- セルフホストGitLabインスタンス
- プロジェクトとコード管理
- CIパイプラインとRunner設定
- バックアップと復元機能

### 5. FG-prompt-pandora (Fargate版サンプルアプリケーション)
- AWS Fargateでの自動スケーリング
- Claude-3.5-Sonnetを活用したプロンプト生成
- Streamlitベースの直感的UI

## 🆕 最新情報

### AMATERASU v1.9.0 (最新のリリース)

- 🎉 **CloudFrontとWAFによるセキュリティ強化**: CloudFrontとWAF v2の導入により、セキュリティが大幅に向上しました。ホワイトリストIPアドレスは`whitelist-waf.exmaple.csv`で管理します。
- 🎉 **ベースインフラのセキュリティグループ設定の改善**: ベースとなるセキュリティグループにデフォルト設定を追加。ホワイトリストからのアクセスを許可するルールを追加。ホワイトリストIPアドレスは`whitelist-base-sg.example.csv`で管理します。
- 🎉 **DeepSeek APIキー設定の追加**: `.env.example`ファイルにDeepSeek APIキーの設定項目を追加しました。
- 🚀 **README.mdファイルの更新**: 各プロジェクトのREADME.mdファイルに、インフラストラクチャ構成、セキュリティ設定、使用方法などの情報を追加・更新しました。バージョン番号を更新しました。
- 🚀 **英語READMEの更新**: 英語のREADMEを更新しました。
- 🚀 **terraform.example.tfvarsへの説明追加**: `terraform.example.tfvars`ファイルに、各変数の役割と設定方法の説明を追加しました。
- 🚀 **terraform.tfvarsの更新**: `terraform.tfvars`ファイルの変数を更新し、`domain`と`subdomain`を追加しました。
- 🚀 **LiteLLM READMEの更新**: セキュリティ強化と構成の簡素化に関する記述を追加しました。
- 🚀 **ベースインフラREADMEの更新**: セキュリティとCloudFront/WAF導入に関する記述に更新しました。
- ⚠️ **インフラストラクチャの大幅な変更**: ALBとCloudFront関連のTerraformモジュールを削除し、インフラストラクチャ構成を簡素化しました。アップグレード前に既存のインフラストラクチャと設定をバックアップしてください。
- ⚠️ **VPC IDとサブネットIDの更新**: LiteLLMプロジェクトのVPC IDとサブネットIDを更新しました。


## 🛠️ 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。


## 📦 インストール手順

1.  リポジトリをクローンします。
2.  各プロジェクトのREADMEに記載されている手順に従って、依存関係をインストールし、アプリケーションをデプロイします。
3.  `terraform.tfvars`ファイルに必要な設定を入力します。


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👏 謝辞

iris-s-coonとMakiの貢献に感謝します。