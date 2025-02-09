#!/bin/bash

# エラー発生時にスクリプトを停止
set -e

# 変数設定
REGION="ap-northeast-1"
ACCOUNT_ID="498218886114"
ECR_REPO="amts-ee-llm-tester-gr"

# 確認プロンプト
echo "⚠️ 警告: ECRリポジトリ '${ECR_REPO}' を完全に削除します。"
echo "この操作は取り消せません。"
read -p "続行しますか？ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ 操作をキャンセルしました。"
    exit 1
fi

# 削除開始メッセージ
echo "🗑️  ECRリポジトリの削除を開始します..."

# リポジトリの存在確認
echo "🔍 ECRリポジトリを確認しています..."
if aws ecr describe-repositories --repository-names ${ECR_REPO} --region ${REGION} 2>/dev/null; then
    # イメージの強制削除
    echo "🧹 リポジトリ内のすべてのイメージを削除しています..."
    aws ecr batch-delete-image \
        --repository-name ${ECR_REPO} \
        --region ${REGION} \
        --image-ids "$(aws ecr list-images \
            --repository-name ${ECR_REPO} \
            --region ${REGION} \
            --query 'imageIds[*]' \
            --output json)"

    # リポジトリの削除
    echo "💥 ECRリポジトリを削除しています..."
    aws ecr delete-repository \
        --repository-name ${ECR_REPO} \
        --region ${REGION} \
        --force

    echo "✅ ECRリポジトリの削除が完了しました。"
else
    echo "❓ 指定されたECRリポジトリは存在しません。"
fi
