# ALBのセキュリティグループ
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for ALB to restrict access from specific IP ranges"
  vpc_id      = var.vpc_id

  # CloudFrontからのHTTP通信許可
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [
      "120.52.22.96/27",
      "205.251.249.0/24",
      "180.163.57.128/26",
      "204.246.168.0/22",
      "205.251.252.0/23",
      "54.192.0.0/16",
      "204.246.173.0/24",
      "54.230.200.0/21",
      "120.253.240.192/26",
      "116.129.226.128/26",
      "130.176.0.0/17",
      "108.156.0.0/14",
      "99.86.0.0/16",
      "205.251.200.0/21",
      "223.71.71.128/25",
      "13.32.0.0/15",
      "120.253.245.128/26",
      "13.224.0.0/14",
      "70.132.0.0/18",
      "15.158.0.0/16",
      "13.249.0.0/16",
      "18.160.0.0/15",
      "205.251.208.0/20",
      "65.9.128.0/18",
      "130.176.128.0/18",
      "58.254.138.0/25",
      "54.230.208.0/20",
      "116.129.226.0/25",
      "52.222.128.0/17",
      "64.252.128.0/18",
      "205.251.254.0/24",
      "54.230.224.0/19",
      "71.152.0.0/17",
      "216.137.32.0/19",
      "204.246.172.0/24",
      "120.52.39.128/27"
    ]
    description = "Allow HTTP traffic from CloudFront"
  }

  # CloudFrontからのHTTPS通信許可
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [
      "120.52.22.96/27",
      "205.251.249.0/24",
      "180.163.57.128/26",
      "204.246.168.0/22",
      "205.251.252.0/23",
      "54.192.0.0/16",
      "204.246.173.0/24",
      "54.230.200.0/21",
      "120.253.240.192/26",
      "116.129.226.128/26",
      "130.176.0.0/17",
      "108.156.0.0/14",
      "99.86.0.0/16",
      "205.251.200.0/21",
      "223.71.71.128/25",
      "13.32.0.0/15",
      "120.253.245.128/26",
      "13.224.0.0/14",
      "70.132.0.0/18",
      "15.158.0.0/16",
      "13.249.0.0/16",
      "18.160.0.0/15",
      "205.251.208.0/20",
      "65.9.128.0/18",
      "130.176.128.0/18",
      "58.254.138.0/25",
      "54.230.208.0/20",
      "116.129.226.0/25",
      "52.222.128.0/17",
      "64.252.128.0/18",
      "205.251.254.0/24",
      "54.230.224.0/19",
      "71.152.0.0/17",
      "216.137.32.0/19",
      "204.246.172.0/24",
      "120.52.39.128/27"
    ]
    description = "Allow HTTPS traffic from CloudFront"
  }

  # VPC内部からのHTTPアクセスを許可
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "Allow HTTP traffic from within VPC"
  }

  # VPC内部からのHTTPSアクセスを許可
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "Allow HTTPS traffic from within VPC"
  }

  # アウトバウンドの通信許可
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

# EC2のセキュリティグループ
resource "aws_security_group" "ec2" {
  name        = "${var.project_name}-ec2-sg"
  description = "Security group for EC2 instance to allow traffic from ALB and SSH access"
  vpc_id      = var.vpc_id

  # SSHの通信許可
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.whitelist_ips
    description = "Allow SSH access from whitelisted IP addresses"
  }

  # HTTPの通信許可
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "Allow HTTP traffic from ALB"
  }

  # HTTPSの通信許可
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "Allow HTTPS traffic from ALB"
  }

  # アウトバウンドの通信許可
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.project_name}-ec2-sg"
  }
}
