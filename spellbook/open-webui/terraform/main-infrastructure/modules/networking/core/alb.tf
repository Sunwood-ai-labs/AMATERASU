# Application Load Balancer の設定

# ALBの作成
resource "aws_lb" "internal" {
  name               = "${var.project_name}-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [var.security_group_id]
  subnets            = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-internal-alb"
  }
}

# HTTPリスナーの作成
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.internal.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }

  depends_on = [
    aws_lb.internal,
    aws_lb_target_group.app
  ]
}

# ターゲットグループの作成（HTTPで受け付け）
resource "aws_lb_target_group" "app" {
  name                          = "${var.project_name}-tg"
  port                          = 80
  protocol                      = "HTTP"
  vpc_id                        = var.vpc_id
  deregistration_delay          = 30
  load_balancing_algorithm_type = "round_robin"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 15
    matcher            = "200-399"
    path               = "/health"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 3
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }

  tags = {
    Name = "${var.project_name}-target-group"
  }
}

# EC2インスタンスをターゲットグループに登録
resource "aws_lb_target_group_attachment" "app" {
  target_group_arn = aws_lb_target_group.app.arn
  target_id        = var.instance_id
  port             = 80
}
