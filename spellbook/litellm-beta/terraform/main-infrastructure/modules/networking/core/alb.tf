# パブリック用ALB
resource "aws_lb" "public" {
  name               = "${var.project_name}-public-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets           = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-public-alb"
  }

  depends_on = [
    aws_acm_certificate_validation.public  ]
}

# 内部用ALB
resource "aws_lb" "internal" {
  name               = "${var.project_name}-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets           = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-internal-alb"
  }

}

# パブリック用ALBターゲットグループ
resource "aws_lb_target_group" "public" {
  name     = "${var.project_name}-public-tg"
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

# 内部用ALBターゲットグループ
resource "aws_lb_target_group" "internal" {
  name     = "${var.project_name}-internal-tg"
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

# EC2インスタンスをパブリックターゲットグループに追加
resource "aws_lb_target_group_attachment" "public" {
  target_group_arn = aws_lb_target_group.public.arn
  target_id        = var.instance_id
  port            = 80
}

# EC2インスタンスを内部用ターゲットグループに追加
resource "aws_lb_target_group_attachment" "internal" {
  target_group_arn = aws_lb_target_group.internal.arn
  target_id        = var.instance_id
  port            = 80
}

# HTTPリスナー（パブリック） - HTTPSにリダイレクト
resource "aws_lb_listener" "public_http" {
  load_balancer_arn = aws_lb.public.arn
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

# HTTPリスナー（内部用） - HTTPSにリダイレクト
resource "aws_lb_listener" "internal_http" {
  load_balancer_arn = aws_lb.internal.arn
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

# HTTPSリスナー（パブリック）
resource "aws_lb_listener" "public_https" {
  load_balancer_arn = aws_lb.public.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.public.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.public.arn
  }

  depends_on = [
    aws_acm_certificate_validation.public
  ]
}

# HTTPSリスナー（内部用）
resource "aws_lb_listener" "internal_https" {
  load_balancer_arn = aws_lb.internal.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.internal.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.internal.arn
  }
}
