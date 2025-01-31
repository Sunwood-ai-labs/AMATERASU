#!/bin/bash

# エラー発生時にスクリプトを停止
set -e

# 変数設定
REGION="ap-northeast-1"
ACCOUNT_ID="498218886114"
ECR_REPO="amts-ee-llm-tester"
IMAGE_TAG="latest"
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
IMAGE_NAME="${ECR_URI}/${ECR_REPO}:${IMAGE_TAG}"
CLUSTER_NAME="amts-ee-llm-tester-cluster"
SERVICE_NAME="amts-ee-llm-tester-service"

# ビルド開始メッセージ
echo "🚀 デプロイを開始します..."

# ECRリポジトリの存在確認と作成
echo "🔍 ECRリポジトリを確認しています..."
if ! aws ecr describe-repositories --repository-names ${ECR_REPO} --region ${REGION} 2>/dev/null; then
    echo "📦 ECRリポジトリを作成しています..."
    aws ecr create-repository \
        --repository-name ${ECR_REPO} \
        --region ${REGION}
fi

# ECRにログイン
echo "📦 ECRにログインしています..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# Dockerイメージをビルド
echo "🔨 Dockerイメージをビルドしています..."
docker build -t ${ECR_REPO}:${IMAGE_TAG} .

# イメージにタグを付ける
echo "🏷️  イメージにタグを付けています..."
docker tag ${ECR_REPO}:${IMAGE_TAG} ${IMAGE_NAME}

# ECRにイメージをプッシュ
echo "⬆️  イメージをECRにプッシュしています..."
docker push ${IMAGE_NAME}

# ECSサービスを更新
echo "🔄 ECSサービスを更新しています..."
aws ecs update-service \
    --cluster ${CLUSTER_NAME} \
    --service ${SERVICE_NAME} \
    --force-new-deployment \
    --region ${REGION}

# デプロイの状態を確認
echo "👀 デプロイの状態を確認しています..."
aws ecs describe-services \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION}

echo "✅ デプロイプロセスが完了しました。"
echo "※ タスクの起動完了まで数分かかる場合があります。"
