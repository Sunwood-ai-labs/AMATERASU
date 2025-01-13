# データソース定義
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
# IAMロール関連
resource "time_rotating" "rotation" {
  rotation_days = 1
}

resource "aws_iam_role" "eventbridge_role" {
  name_prefix = "${var.project_name}-eventbridge-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    rotation = time_rotating.rotation.id
  }
}

resource "aws_iam_role_policy_attachment" "ssm_automation_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonSSMAutomationRole"
  role       = aws_iam_role.eventbridge_role.name
}

# ネットワークインターフェース
resource "aws_network_interface" "app_server" {
  subnet_id       = var.public_subnet_id
  security_groups = var.security_group_ids

  tags = {
    Name = "${var.project_name}-eni"
  }
}

# EC2インスタンス
resource "aws_instance" "app_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  iam_instance_profile   = var.iam_instance_profile
  key_name               = var.key_name

  # ネットワークインターフェースをアタッチ
  network_interface {
    network_interface_id = aws_network_interface.app_server.id
    device_index        = 0
  }

  root_block_device {
    volume_type = "gp2"
    volume_size = 50
  }

  user_data = templatefile(var.setup_script_path, {
    env_content = file(var.env_file_path)
  })

  tags = {
    Name = "${var.project_name}-ec2"
  }
}

# Elastic IP
resource "aws_eip" "app_server" {
  domain = "vpc"
  network_interface = aws_network_interface.app_server.id

  tags = {
    Name = "${var.project_name}-eip"
  }
}

# CloudWatchイベント
resource "aws_cloudwatch_event_rule" "start_instance" {
  name                = "${var.project_name}-start-instance"
  description         = "Start the EC2 instance at 8 AM Japan time"
  schedule_expression = "cron(0 6 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "start_instance" {
  rule      = aws_cloudwatch_event_rule.start_instance.name
  target_id = "start_instance"
  arn       = "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:automation-definition/AWS-StartEC2Instance"
  role_arn  = aws_iam_role.eventbridge_role.arn

  input = jsonencode({
    InstanceId = [aws_instance.app_server.id]
  })
}

resource "aws_cloudwatch_event_rule" "stop_instance" {
  name                = "${var.project_name}-stop-instance"
  description         = "Stop the EC2 instance at 4 PM Japan time"
  schedule_expression = "cron(0 7 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "stop_instance" {
  rule      = aws_cloudwatch_event_rule.stop_instance.name
  target_id = "stop_instance"
  arn       = "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:automation-definition/AWS-StopEC2Instance"
  role_arn  = aws_iam_role.eventbridge_role.arn

  input = jsonencode({
    InstanceId = [aws_instance.app_server.id]
  })
}
