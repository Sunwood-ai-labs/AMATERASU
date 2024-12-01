# modules/networking/alb/main.tf

# パブリックALB（外部アクセス用）
resource "aws_lb" "public" {
  name               = "${var.project_name}-public-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]  # 既存のセキュリティグループを使用
  subnets            = [var.public_subnet_id, var.public_subnet_2_id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-public-alb"
  }
}

# インターナルALB（VPC内部アクセス用）
resource "aws_lb" "internal" {
  name               = "${var.project_name}-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]  # 同じセキュリティグループを使用
  subnets            = [var.public_subnet_id, var.public_subnet_2_id]  # 同じサブネットを使用

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-internal-alb"
  }
}

# 以下のターゲットグループとリスナーの設定は変更なし
# パブリックALB用ターゲットグループ
resource "aws_lb_target_group" "public" {
  name        = "${var.project_name}-public-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200"
    path               = "/"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name = "${var.project_name}-public-tg"
  }
}

# インターナルALB用ターゲットグループ
resource "aws_lb_target_group" "internal" {
  name        = "${var.project_name}-internal-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200"
    path               = "/"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name = "${var.project_name}-internal-tg"
  }
}
