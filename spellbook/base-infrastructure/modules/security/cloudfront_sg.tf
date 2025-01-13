resource "aws_security_group" "cloudfront" {
  name_prefix = "${var.project_name}-cloudfront-sg"
  description = "CloudFront security group for ${var.project_name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 443
    protocol    = "tcp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.cloudfront.id]
    description = "Allow HTTP/HTTPS access from CloudFront"
  }

  tags = merge(
    {
      Name        = "${var.project_name}-cloudfront-sg"
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
