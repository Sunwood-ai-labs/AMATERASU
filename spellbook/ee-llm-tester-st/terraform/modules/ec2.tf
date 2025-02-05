# EC2インスタンス用のElastic IP
resource "aws_eip" "ecs_instance" {
  domain = "vpc"
  tags = {
    Name = "${var.project_name}-eip"
  }
}

# EC2インスタンスのLaunch Template
resource "aws_launch_template" "ecs" {
  name_prefix   = "${var.project_name}-template"
  image_id      = var.ecs_ami_id
  instance_type = var.instance_type

  network_interfaces {
    associate_public_ip_address = true
    security_groups            = [aws_security_group.ecs_tasks.id]  # 直接セキュリティグループを参照
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              echo "ECS_CLUSTER=${aws_ecs_cluster.main.name}" >> /etc/ecs/ecs.config
              EOF
  )

  key_name = var.ec2_key_name

  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_instance_profile.name
  }

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project_name}-ecs-instance"
    }
  }
}

# SSM Association
resource "aws_ssm_association" "ssm_association" {
  name = "AWS-RunShellScript"
  
  targets {
    key    = "tag:Name"
    values = ["${var.project_name}-ecs-instance"]
  }
  
  parameters = {
    commands = "#!/bin/bash\necho 'SSM Agent is running'\ndate"
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "ecs" {
  name                = "${var.project_name}-asg"
  desired_capacity    = 1
  max_size           = 1
  min_size           = 1
  target_group_arns  = [aws_lb_target_group.ecs.arn]
  vpc_zone_identifier = [var.public_subnet_id]

  launch_template {
    id      = aws_launch_template.ecs.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-ecs-instance"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}
