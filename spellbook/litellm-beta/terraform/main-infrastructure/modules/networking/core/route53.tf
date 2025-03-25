# ACM証明書の作成 (CloudFront用 - us-east-1)
resource "aws_acm_certificate" "cert" {
  provider = aws.us_east_1
  domain_name       = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"

  tags = {
    Name = "${var.project_name}-cloudfront-certificate"
  }
}

# ACM証明書の作成 (ALB用 - ap-northeast-1)
resource "aws_acm_certificate" "alb_cert" {
  provider = aws
  domain_name       = "${var.subdomain}.${var.domain}"
  validation_method = "DNS"
  # subject_alternative_names = ["${var.subdomain}.${var.domain_internal}"]

  tags = {
    Name = "${var.project_name}-certificate"
  }

  lifecycle {
    create_before_destroy = true
  }

}

# 証明書検証用のDNSレコード
resource "aws_route53_record" "alb_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.alb_cert.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
    }
  }

  zone_id = data.aws_route53_zone.public.id
  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
  ttl     = 30

  provider        = aws
  allow_overwrite = true

  lifecycle {
    create_before_destroy = true
  }
}

# 証明書の検証完了を待つ
resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn         = aws_acm_certificate.alb_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.alb_cert_validation : record.fqdn]
  
  depends_on = [
    aws_route53_record.alb_cert_validation,
    aws_acm_certificate.alb_cert
  ]

  lifecycle {
    create_before_destroy = true
  }
}

# ALBの作成
resource "aws_lb" "app" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets           = [var.public_subnet_id, var.public_subnet_2_id]

  tags = {
    Name = "${var.project_name}-alb"
  }

  depends_on = [
    aws_acm_certificate_validation.cert_validation,
    time_sleep.dns_propagation
  ]
}

# DNSの伝播を待つための遅延
resource "time_sleep" "dns_propagation" {
  depends_on = [aws_route53_record.alb_cert_validation]

  # 待機時間を延長 (2分から10分に)
  create_duration  = "600s"  # 10分待機
  destroy_duration = "30s"
}

# ALBターゲットグループ
resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    timeout            = 5
    path               = "/"
    port               = "traffic-port"
    protocol           = "HTTP"
  }
}

# EC2インスタンスをターゲットグループに追加
resource "aws_lb_target_group_attachment" "app" {
  target_group_arn = aws_lb_target_group.app.arn
  target_id        = var.instance_id
  port            = 80
}

# HTTPリスナー - HTTPSにリダイレクト
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# HTTPSリスナー
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate_validation.cert_validation.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }

  depends_on = [
    aws_acm_certificate_validation.cert_validation
  ]
}

# 内部DNSレコード
resource "aws_route53_record" "private_http" {
  zone_id = var.route53_internal_zone_id
  name    = "${var.subdomain}.${var.domain_internal}"
  type    = "A"
  allow_overwrite = true

  alias {
    name                   = aws_lb.app.dns_name
    zone_id                = aws_lb.app.zone_id
    evaluate_target_health = true
  }
}

# パブリックDNSレコード
resource "aws_route53_record" "alb" {
  zone_id = data.aws_route53_zone.public.id
  name    = "${var.subdomain}.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_lb.app.dns_name
    zone_id                = aws_lb.app.zone_id
    evaluate_target_health = true
  }
}
