#!/bin/bash

# エラー発生時にスクリプトを停止
set -e

# 変数設定
REGION="ap-northeast-1"
ACCOUNT_ID="498218886114"
ECR_REPO="amts-prompt-pandora"
IMAGE_TAG="latest"
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
IMAGE_NAME="${ECR_URI}/${ECR_REPO}:${IMAGE_TAG}"
CLUSTER_NAME="amts-prompt-pandora-cluster"
SERVICE_NAME="amts-prompt-pandora-service"

echo "ECRにログインしています..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}

echo "ECRリポジトリを作成しています..."
aws ecr create-repository --repository-name ${ECR_REPO} --region ${REGION} || true

echo "Dockerイメージをビルドしています..."
docker build -t ${ECR_REPO}:${IMAGE_TAG} .

echo "イメージにタグを付けています..."
docker tag ${ECR_REPO}:${IMAGE_TAG} ${IMAGE_NAME}

echo "イメージをECRにプッシュしています..."
docker push ${IMAGE_NAME}

echo "ECSサービスを更新しています..."
aws ecs update-service --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME} --force-new-deployment --region ${REGION}

echo "デプロイの状態を確認しています..."
aws ecs describe-services --cluster ${CLUSTER_NAME} --services ${SERVICE_NAME} --region ${REGION}

echo "更新プロセスが完了しました。"
