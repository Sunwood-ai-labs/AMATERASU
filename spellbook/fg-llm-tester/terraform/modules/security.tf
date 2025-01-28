# ECSタスク用セキュリティグループの作成
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-sg-ecs-tasks"
  description = "ECS tasks security group"
  vpc_id      = var.vpc_id

  # CloudFrontからの80番ポートへのアクセスを許可
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # CloudFrontのIPレンジは動的に変更されるため
    description = "Allow inbound traffic from CloudFront"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.project_name}-sg-ecs-tasks"
  }
}
