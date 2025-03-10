output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.app_server.public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_network_interface.app_server.private_ip
}

output "instance_private_dns" {
  description = "Private DNS hostname of the EC2 instance"
  value       = aws_instance.app_server.private_dns
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.app_server.public_dns
}

output "elastic_ip" {
  description = "Elastic IP address assigned to the instance"
  value       = aws_eip.app_server.public_ip
}
