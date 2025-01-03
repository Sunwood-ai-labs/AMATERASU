# データソース定義
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_security_group" "existing" {
  id = var.security_group_id
}

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

# EC2インスタンス
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

  user_data = templatefile(var.setup_script_path, {
    env_content = file(var.env_file_path)
  })

  tags = {
    Name = "${var.project_name}-ec2"
  }
}

# Elastic IP
resource "aws_eip" "app_server" {
  instance = aws_instance.app_server.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

# セキュリティグループルール
resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = var.security_group_id
  cidr_ipv4        = "10.0.0.0/16"  # VPC内からのみアクセスを許可
  ip_protocol      = "tcp"
  description      = "Allow HTTP inbound traffic from VPC"
  from_port        = 80
  to_port          = 80

  tags = {
    Name = "${var.project_name}-http-rule"
  }
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = var.security_group_id
  cidr_ipv4        = "10.0.0.0/16"  # VPC内からのみアクセスを許可
  ip_protocol      = "tcp"
  description      = "Allow HTTPS inbound traffic from VPC"
  from_port        = 443
  to_port          = 443

  tags = {
    Name = "${var.project_name}-https-rule"
  }
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  security_group_id = var.security_group_id
  cidr_ipv4        = "0.0.0.0/0"  # SSHは管理用に外部からのアクセスを許可
  ip_protocol      = "tcp"
  description      = "Allow SSH inbound traffic"
  from_port        = 22
  to_port          = 22

  tags = {
    Name = "${var.project_name}-ssh-rule"
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
