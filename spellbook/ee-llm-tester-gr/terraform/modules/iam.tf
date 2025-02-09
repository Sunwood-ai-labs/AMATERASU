# EC2インスタンスプロファイル用ロール
resource "aws_iam_role" "ecs_instance_role" {
  name = "${var.project_name}-ecs-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# EC2インスタンスプロファイル
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "${var.project_name}-ecs-instance-profile"
  role = aws_iam_role.ecs_instance_role.name
}

# ECSエージェント用ポリシー
resource "aws_iam_role_policy_attachment" "ecs_instance_role_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# SSM Managed Instance Coreポリシー
resource "aws_iam_role_policy_attachment" "ecs_instance_role_ssm_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# ECSタスクロール
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Bedrockフルアクセスポリシー
resource "aws_iam_policy" "bedrock_full_access" {
  name = "${var.project_name}-bedrock-full-access"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "bedrock:*",
        Resource = "*"
      }
    ]
  })
}

# ECSタスクロールへのポリシーアタッチ
resource "aws_iam_role_policy_attachment" "ecs_task_role_bedrock_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.bedrock_full_access.arn
}

# ECS実行ロール
resource "aws_iam_role" "ecs_execution_role" {
  name = "${var.project_name}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# ECS実行ロールへの基本ポリシーのアタッチ
resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ElasticIPをアタッチするためのポリシー
resource "aws_iam_role_policy" "ecs_instance_role_policy" {
  name = "${var.project_name}-eip-policy"
  role = aws_iam_role.ecs_instance_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:AssociateAddress",
          "ec2:DescribeAddresses"
        ]
        Resource = "*"
      }
    ]
  })
}

# 出力定義
output "ecs_task_role_arn" {
  value       = aws_iam_role.ecs_task_role.arn
  description = "The ARN of the ECS task role"
}

output "ecs_execution_role_arn" {
  value       = aws_iam_role.ecs_execution_role.arn
  description = "The ARN of the ECS execution role"
}
