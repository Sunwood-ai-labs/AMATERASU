#!/bin/bash

# エラー発生時にスクリプトを停止
set -e

# 変数設定
PROJECT_NAME="amts-llm-tester"
VPC_ID="vpc-02f238431c68567d5"
REGION="ap-northeast-1"
ACCOUNT_ID="498218886114"

echo "🔄 既存リソースをTerraform stateにインポートします..."

# IAMロール
echo "📦 IAMロールをインポート中..."
terraform import "module.main.aws_iam_role.ecs_instance_role" "${PROJECT_NAME}-ecs-instance-role"
terraform import "module.main.aws_iam_role.ecs_task_role" "${PROJECT_NAME}-ecs-task-role"
terraform import "module.main.aws_iam_role.ecs_execution_role" "${PROJECT_NAME}-ecs-execution-role"

# IAMポリシー
echo "📦 IAMポリシーをインポート中..."
terraform import "module.main.aws_iam_policy.bedrock_full_access" "arn:aws:iam::${ACCOUNT_ID}:policy/${PROJECT_NAME}-bedrock-full-access"

# セキュリティグループ
echo "📦 セキュリティグループをインポート中..."
SG_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=${PROJECT_NAME}-sg-alb" --query 'SecurityGroups[0].GroupId' --output text)
terraform import "module.main.aws_security_group.alb" "$SG_ID"

# IAMインスタンスプロファイル
echo "📦 IAMインスタンスプロファイルをインポート中..."
terraform import "module.main.aws_iam_instance_profile.ecs_instance_profile" "${PROJECT_NAME}-ecs-instance-profile"

# CloudWatch Logs
echo "📦 CloudWatchロググループをインポート中..."
terraform import "module.main.aws_cloudwatch_log_group.ecs" "/ecs/${PROJECT_NAME}"

# セキュリティグループ
echo "📦 セキュリティグループをインポート中..."
SG_ID=$(aws ec2 describe-security-groups \
  --region ${REGION} \
  --filters "Name=group-name,Values=${PROJECT_NAME}-sg-alb" \
  --query 'SecurityGroups[0].GroupId' \
  --output text)
terraform import "module.main.aws_security_group.alb" "$SG_ID"

# ターゲットグループ
echo "📦 ALBターゲットグループをインポート中..."
TG_ARN=$(aws elbv2 describe-target-groups \
  --region ${REGION} \
  --names "${PROJECT_NAME}-tg" \
  --query 'TargetGroups[0].TargetGroupArn' \
  --output text)
terraform import "module.main.aws_lb_target_group.ecs" "$TG_ARN"

# WAF IPセット
echo "📦 WAF IPセットをインポート中..."
IP_SET_ID=$(aws wafv2 list-ip-sets \
  --scope CLOUDFRONT \
  --region us-east-1 \
  --query "IPSets[?Name=='${PROJECT_NAME}-whitelist'].Id" \
  --output text)
IP_SET_NAME="${PROJECT_NAME}-whitelist"
if [ ! -z "$IP_SET_ID" ]; then
  terraform import "module.main.aws_wafv2_ip_set.whitelist" "us-east-1/${IP_SET_ID}/${IP_SET_NAME}/CLOUDFRONT"
else
  echo "WAF IPセットが見つかりません"
fi

echo "✅ インポート完了"
echo "terraform plan を実行して差分を確認してください"
