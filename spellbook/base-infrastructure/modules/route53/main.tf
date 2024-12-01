# modules/route53/main.tf
resource "aws_route53_zone" "private" {
  name = var.domain_name

  vpc {
    vpc_id = var.vpc_id
  }

  tags = merge(
    {
      Name        = "${var.project_name}-route53-zone"
      Environment = var.environment
    },
    var.tags
  )
}
