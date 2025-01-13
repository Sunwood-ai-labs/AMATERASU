output "instance_id" {
  description = "ID of the EC2 instance"
  value       = module.compute.instance_id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.compute.instance_public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = module.compute.instance_private_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = module.compute.instance_public_dns
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = module.networking.public_subnet_id
}

output "dns_record_info" {
  description = "プライベートホストゾーンのDNSレコード情報"
  value       = module.networking.dns_record_info
}

output "internal_access_info" {
  description = "VPC内部からのアクセス情報"
  value       = <<-EOT
    VPC内のインスタンスから以下のURLでアクセスできます：
    https://${var.subdomain}.${var.domain_internal}

    セキュリティ対策：
    - HTTPS通信によるエンドツーエンドの暗号化
    - ACM証明書によるサーバー認証
    - VPC内部でも安全な通信を確保
    - セキュリティグループ（${var.security_group_id}）による通信制御

    注意：
    - このURLはVPC内部からのみアクセス可能です
    - HTTPアクセスは自動的にHTTPSにリダイレクトされます
    - 外部からのアクセスはできません
  EOT
}
