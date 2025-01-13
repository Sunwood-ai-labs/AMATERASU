resource "aws_security_group" "vpc_internal" {
  name_prefix = "${var.project_name}-vpc-internal-sg"
  description = "VPC internal security group for ${var.project_name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Allow all traffic within VPC"
  }

  tags = merge(
    {
      Name        = "${var.project_name}-vpc-internal-sg"
      Environment = var.environment
    },
    var.tags
  )

  lifecycle {
    create_before_destroy = true
  }
}
