<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">エンタープライズグレードのプライベートAIプラットフォーム (v1.11.0)</h2>

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

### AMATERASU v1.11.0 (最新のリリース)

- 🎉 **WAFv2によるIPホワイトリスト設定**: AWS WAFv2を使用して、CloudFrontへのアクセスを制御するIPホワイトリスト機能を実装しました。`whitelist-waf.csv`ファイルからIPアドレスを読み込み、`aws_wafv2_ip_set`リソースを使用してIPセットを作成しています。デフォルトではアクセスをブロックし、ホワイトリストに登録されたIPアドレスからのアクセスのみ許可する設定となっています。(commit: 57883b3)
- 🎉 **CloudFrontインフラ構築用README.md作成**: OpenWebUIをEC2上で動作させるためのCloudFrontインフラ構築手順を記述したREADME.mdを追加しました。CloudFront、WAFv2、Route53の設定方法、前提条件、セットアップ手順、出力値、環境削除方法、注意事項、トラブルシューティングなどを網羅的に解説しています。(commit: b275845)
- 🎉 **Route53によるDNSレコード設定**: CloudFrontディストリビューション用のエイリアスレコードをRoute53に自動的に作成する設定を追加しました。(commit: 105d6a6)
- 🎉 **CloudFront関連出力値定義**: CloudFrontディストリビューションのドメイン名、ID、ARN、URLなどの重要な情報を取得するための出力値を定義しました。(commit: 27df674)
- 🎉 **ACM証明書とDNS検証の自動化**: CloudFrontに使用するACM証明書の自動作成と、Route53を使ったDNS検証機能を実装しました。(commit: 6ad223a)
- 🎉 **セキュリティグループ設定の強化とAMI IDの明示化**: セキュリティグループIDを単一IDから複数のIDのリストに変更しました。(commit: 5897676)
- 🎉 **セキュリティグループIDの出力追加**: `outputs.tf`にセキュリティグループIDを出力する項目を追加しました。(commit: 6e97f07)
- 🎉 **ホワイトリストサンプルCSV追加**: WAFのホワイトリスト設定用サンプルCSVファイルを追加しました。(commit: 49dd8b4)
- 🚀 **プロバイダー設定の統合**: `provider.tf`を`main.tf`に統合し、ファイル数を削減しました。(commit: 7f9dfd6)
- 🚀 **tfvarsファイルの例を追加**: 環境変数を設定するための`terraform.example.tfvars`ファイルを追加しました。(commit: fc59dcd)
- 🐛 **WAF設定のホワイトリストCSVパスを修正**: WAF設定で参照するホワイトリストCSVファイルのパスを修正しました。(commit: f6254c4)
- ⚠️ **インフラストラクチャの大幅な変更**: 既に実装されている機能の改善やリファクタリングが行われています。既存のインフラストラクチャと設定をバックアップしてからアップグレードしてください。


## 🛠️ 使用方法

各コンポーネントの使用方法については、それぞれのREADMEファイルを参照してください。


## 📦 インストール手順

1.  リポジトリをクローンします。
2.  各プロジェクトのREADMEに記載されている手順に従って、依存関係をインストールし、アプリケーションをデプロイします。
3.  `terraform.tfvars`ファイルに必要な設定を入力します。


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👏 謝辞

Maki、iris-s-coonへの貢献に感謝します。