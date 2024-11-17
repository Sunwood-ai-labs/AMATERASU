# modules/security/main.tf
resource "aws_security_group" "default" {
  name_prefix = "${var.project_name}-default-sg"
  description = "Default security group for ${var.project_name}"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "${ingress.value.description} - SSH Access"
    }
  }

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "${ingress.value.description} - HTTP Access"
    }
  }

  dynamic "ingress" {
    for_each = var.whitelist_entries
    content {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = [ingress.value.ip]
      description = "${ingress.value.description} - HTTPS Access"
    }
  }

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
