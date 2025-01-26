# ECSタスク用セキュリティグループの作成
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-sg-ecs-tasks"
  description = "ECS tasks security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = -1
    security_groups = var.security_group_ids
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg-ecs-tasks"
  }
}

# 出力定義
output "ecs_tasks_security_group_id" {
  value       = aws_security_group.ecs_tasks.id
  description = "The ID of the ECS tasks security group"
}
