resource "aws_security_group_rule" "allow_all_traffic_from_eip" {
    type              = "ingress"
    from_port         = 0
    to_port           = 65535
    protocol          = "-1"
    cidr_blocks       = ["${var.instance_public_ip}/32"]
    security_group_id = var.security_group_ids[0]  # デフォルトセキュリティグループを使用
    description       = "Allow all traffic from Elastic IP for ${var.project_name}"
}
