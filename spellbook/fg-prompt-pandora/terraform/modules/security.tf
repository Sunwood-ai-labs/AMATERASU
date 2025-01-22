# ECSタスク用セキュリティグループの作成
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-sg-ecs-tasks"
  description = "ECS tasks security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 8501
    to_port         = 8501
    protocol        = "tcp"
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

# NAT Gateway用Elastic IP
resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name = "${var.project_name}-nat-eip"
  }
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = var.public_subnet_id

  tags = {
    Name = "${var.project_name}-nat-gateway"
  }
}

# 出力定義
output "ecs_tasks_security_group_id" {
  value       = aws_security_group.ecs_tasks.id
  description = "The ID of the ECS tasks security group"
}

output "nat_gateway_ip" {
  value       = aws_eip.nat.public_ip
  description = "The Elastic IP address of the NAT Gateway"
}
