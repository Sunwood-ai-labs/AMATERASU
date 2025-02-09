# ECSクラスターの作成
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# ECSタスク定義
resource "aws_ecs_task_definition" "app" {
  family                = "${var.project_name}-task"
  network_mode         = "bridge"
  execution_role_arn   = aws_iam_role.ecs_execution_role.arn
  task_role_arn        = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "${var.project_name}-container"
      image = var.container_image
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      essential = true
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/${var.project_name}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      memory = 512,
      memoryReservation = 256
    }
  ])
}

# CloudWatch Logsグループ
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 30
}

# ECSサービス
resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "EC2"

  # EC2インスタンスのElastic IPをCloudFrontのオリジンとして使用
  load_balancer {
    target_group_arn = aws_lb_target_group.ecs.arn
    container_name   = "${var.project_name}-container"
    container_port   = 80
  }

  force_new_deployment = true

  depends_on = [aws_lb_listener.front_end]
}
