resource "aws_security_group" "default" {
  name_prefix = "${var.project_name}-default-sg"
  description = "Default security group for ${var.project_name}"
  vpc_id      = var.vpc_id

  # 外部からのアクセスはホワイトリストIPからの特定ポートのみ許可
  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "SSH access from ${ingress.value.description}"
    }
  }

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 2222
      to_port     = 2222
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "gitlab access from ${ingress.value.description}"
    }
  }

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "HTTP access from ${ingress.value.description}"
    }
  }

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "HTTPS access from ${ingress.value.description}"
    }
  }

  # VPC内の全トラフィックを許可（全ポート）
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Allow all traffic within VPC"
  }

  # 全ての送信トラフィックを許可
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(
    {
      Name        = "${var.project_name}-default-sg"
      Environment = var.environment
    },
    var.tags
  )

  lifecycle {
    create_before_destroy = true
  }
}
