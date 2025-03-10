# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets           = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false
}

# ALBリスナー
resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs.arn
  }
}

# ALBターゲットグループ
resource "aws_lb_target_group" "ecs" {
  name     = "${var.project_name}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200"
    path               = "/"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 10
  }
}

# EC2インスタンスをターゲットグループに登録
resource "aws_lb_target_group_attachment" "ecs" {
  target_group_arn = aws_lb_target_group.ecs.arn
  target_id        = aws_instance.ecs.id
  port             = 80
}

