resource "aws_security_group" "whitelist" {
  name_prefix = "${var.project_name}-whitelist-sg"
  description = "Whitelist security group for ${var.project_name}"
  vpc_id      = var.vpc_id

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

  tags = merge(
    {
      Name        = "${var.project_name}-whitelist-sg"
      Environment = var.environment
    },
    var.tags
  )

  lifecycle {
    create_before_destroy = true
  }
}
