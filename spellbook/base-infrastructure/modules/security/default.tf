resource "aws_security_group" "default" {
  name_prefix = "${var.project_name}-default-sg"
  description = "Default security group for ${var.project_name}"
  vpc_id      = var.vpc_id

  # ホワイトリストからのアクセスを許可
  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 0
      to_port     = 0
      protocol    = -1
      cidr_blocks = [ingress.value.ip]
      description = "All access from ${ingress.value.description}"
    }
  }

  # クラウドフロントからのHTTP/HTTPSアクセスを許可
  ingress {
    from_port   = 80
    to_port     = 443
    protocol    = "tcp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.cloudfront.id]
    description = "Allow HTTP/HTTPS access from CloudFront"
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

data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}
