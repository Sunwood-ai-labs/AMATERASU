resource "aws_security_group" "default" {
  name_prefix = "${var.project_name}-default-sg"
  description = "Default security group to control access from whitelisted IPs, CloudFront, and VPC internal resources"
  vpc_id      = var.vpc_id

  # Allow traffic from whitelisted IP addresses
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.whitelist.id]
    description     = "Allow all traffic from whitelisted IP addresses for management and monitoring"
  }

  # Allow traffic from CloudFront edge locations
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.cloudfront.id]
    description     = "Allow all traffic from CloudFront edge locations for content delivery"
  }

  # Allow traffic from VPC internal resources
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.vpc_internal.id]
    description     = "Allow all traffic from internal VPC resources for inter-service communication"
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic for internet access"
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
