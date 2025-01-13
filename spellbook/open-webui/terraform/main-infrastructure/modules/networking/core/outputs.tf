output "vpc_id" {
  description = "ID of the VPC"
  value       = module.data_sources.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.data_sources.vpc_cidr
}

output "public_subnet_id" {
  description = "ID of the first public subnet"
  value       = module.data_sources.public_subnet_id
}

output "public_subnet_2_id" {
  description = "ID of the second public subnet"
  value       = module.data_sources.public_subnet_2_id
}

output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = var.security_group_id
}

output "dns_record_info" {
  description = "プライベートホストゾーンのDNSレコード情報"
  value = {
    domain = "${var.subdomain}.${var.domain_internal}"
    type   = "A"
    alb_dns_name = aws_lb.internal.dns_name
    alb_zone_id  = aws_lb.internal.zone_id
    status = "ALBにエイリアス設定済み"
  }
}

output "alb_info" {
  description = "Application Load Balancer情報"
  value = {
    dns_name = aws_lb.internal.dns_name
    zone_id  = aws_lb.internal.zone_id
    arn      = aws_lb.internal.arn
    target_group_arn = aws_lb_target_group.app.arn
    https_listener_arn = aws_lb_listener.https.arn
    http_listener_arn  = aws_lb_listener.http.arn
    certificate_arn = aws_acm_certificate.alb.arn
  }
}

output "certificate_info" {
  description = "証明書情報"
  value = {
    alb_cert_arn = aws_acm_certificate.alb.arn
    domain = "${var.subdomain}.${var.domain}"
    status = "パブリックCA発行の証明書"
    validation_method = "DNS"
  }
}

output "target_group_info" {
  description = "ターゲットグループ情報"
  value = {
    name = aws_lb_target_group.app.name
    arn  = aws_lb_target_group.app.arn
    port = aws_lb_target_group.app.port
    protocol = aws_lb_target_group.app.protocol
  }
}
