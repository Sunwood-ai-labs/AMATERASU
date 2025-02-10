# EC2インスタンス用のElastic IP
resource "aws_eip" "ecs_instance" {
  domain = "vpc"
  tags = {
    Name = "${var.project_name}-eip"
  }
}

# EC2インスタンス
resource "aws_instance" "ecs" {
  ami           = var.ecs_ami_id
  instance_type = var.instance_type
  subnet_id     = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.ecs_tasks.id]
  key_name      = var.ec2_key_name
  
  user_data = base64encode(<<-EOF
              #!/bin/bash
              echo "ECS_CLUSTER=${aws_ecs_cluster.main.name}" >> /etc/ecs/ecs.config
              EOF
  )

  iam_instance_profile = aws_iam_instance_profile.ecs_instance_profile.name

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name = "${var.project_name}-ecs-instance"
  }

  monitoring = true

  lifecycle {
    create_before_destroy = true
  }
}

# EIPをEC2インスタンスに関連付け
resource "aws_eip_association" "ecs_eip" {
  instance_id   = aws_instance.ecs.id
  allocation_id = aws_eip.ecs_instance.id
}

# SSM Association
resource "aws_ssm_association" "ssm_association" {
  name = "AWS-RunShellScript"
  
  targets {
    key    = "InstanceIds"
    values = [aws_instance.ecs.id]
  }
  
  parameters = {
    commands = "#!/bin/bash\necho 'SSM Agent is running'\ndate"
  }
}
