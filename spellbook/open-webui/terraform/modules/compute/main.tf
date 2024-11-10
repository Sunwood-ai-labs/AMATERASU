resource "aws_instance" "app_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [var.security_group_id]
  iam_instance_profile   = var.iam_instance_profile
  key_name               = var.key_name

  root_block_device {
    volume_type = "gp2"
    volume_size = 50
  }

  user_data = templatefile("${path.module}/../../scripts/setup_script.sh", {
    env_content = file("${path.module}/../../.env")
  })

  tags = {
    Name = "${var.project_name}-ec2"
  }
}

resource "aws_cloudwatch_event_rule" "start_instance" {
  name                = "${var.project_name}-start-instance"
  description         = "Start the EC2 instance at 8 AM Japan time"
  schedule_expression = "cron(0 23 ? * SUN-THU *)"
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

resource "aws_iam_role" "eventbridge_role" {
  name = "${var.project_name}-eventbridge-role"

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
}

resource "aws_iam_role_policy_attachment" "ssm_automation_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonSSMAutomationRole"
  role       = aws_iam_role.eventbridge_role.name
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
