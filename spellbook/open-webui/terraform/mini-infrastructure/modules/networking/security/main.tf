# ALBのセキュリティグループ
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for ALB to restrict access from specific IP ranges"
  vpc_id      = var.vpc_id

  # HTTPの通信許可（ホワイトリストからのアクセスのみ）
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.whitelist_ips
    description = "Allow HTTP traffic from whitelisted IP addresses"
  }

  # HTTPSの通信許可（ホワイトリストからのアクセスのみ）
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.whitelist_ips
    description = "Allow HTTPS traffic from whitelisted IP addresses"
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
