# ECSクラスターの作成
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# タスク定義の作成
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "${var.project_name}-container"
      image = var.container_image
      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]
      essential = true
    }
  ])
}

# ECSサービスの作成
resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id, data.aws_security_group.existing.id]
    subnets         = [var.public_subnet_id, var.public_subnet_2_id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "${var.project_name}-container"
    container_port   = 8501
  }

  depends_on = [aws_lb_listener.https]
}

# Application Auto Scaling Target の設定
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = var.app_count
  min_capacity       = 0
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# 平日朝8時に起動するスケジュール
resource "aws_appautoscaling_scheduled_action" "start" {
  name               = "start-weekday"
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  schedule          = "cron(0 23 ? * SUN-THU *)"  # UTC 23:00 = JST 08:00

  scalable_target_action {
    min_capacity = var.app_count
    max_capacity = var.app_count
  }
}

# 平日夜10時に停止するスケジュール
resource "aws_appautoscaling_scheduled_action" "stop" {
  name               = "stop-weekday"
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  schedule          = "cron(0 13 ? * MON-FRI *)"  # UTC 13:00 = JST 22:00

  scalable_target_action {
    min_capacity = 0
    max_capacity = 0
  }
}

# 出力定義
output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = aws_ecs_service.app.name
  description = "The name of the ECS service"
}
