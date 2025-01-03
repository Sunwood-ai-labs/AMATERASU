# modules/networking/alb/main.tf

# ALBの作成
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-alb"
  }
}

# ターゲットグループの作成
resource "aws_lb_target_group" "main" {
  name        = "${var.project_name}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200-399"
    path               = "/health"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 2
  }

  # コンテナの起動時間を考慮
  deregistration_delay = 60

  # スティッキーセッションの設定
  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }

  tags = {
    Name = "${var.project_name}-tg"
  }
}

# HTTPSリスナーの作成
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Invalid request"
      status_code  = "403"
    }
  }
}

# HTTPSリスナールール - カスタムヘッダーの検証（シークレットIDが指定されている場合のみ）
resource "aws_lb_listener_rule" "verify_header" {
  count = var.origin_secret_id != null ? 1 : 0

  listener_arn = aws_lb_listener.https.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }

  condition {
    http_header {
      http_header_name = "X-Origin-Verify"
      values           = [data.aws_secretsmanager_secret_version.origin_secret[0].secret_string]
    }
  }
}

# HTTPリスナーの作成（HTTPSへのリダイレクト）
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
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

# CloudWatchメトリクスアラーム（SNSトピックが指定されている場合のみ作成）
resource "aws_cloudwatch_metric_alarm" "unhealthy_hosts" {
  count = var.sns_topic_arn != null ? 1 : 0

  alarm_name          = "${var.project_name}-unhealthy-hosts"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "UnHealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period             = "300"
  statistic          = "Average"
  threshold          = "0"
  alarm_description  = "Number of unhealthy hosts in target group"
  
  dimensions = {
    TargetGroup  = aws_lb_target_group.main.arn_suffix
    LoadBalancer = aws_lb.main.arn_suffix
  }

  alarm_actions = [var.sns_topic_arn]
}

# CloudFrontからのOrigin認証シークレットを取得（シークレットIDが指定されている場合のみ）
data "aws_secretsmanager_secret_version" "origin_secret" {
  count = var.origin_secret_id != null ? 1 : 0
  secret_id = var.origin_secret_id
}
