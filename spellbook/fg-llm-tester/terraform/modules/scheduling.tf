# Auto Scaling Target
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
output "autoscaling_target_id" {
  value       = aws_appautoscaling_target.ecs_target.id
  description = "The ID of the Auto Scaling Target"
}
