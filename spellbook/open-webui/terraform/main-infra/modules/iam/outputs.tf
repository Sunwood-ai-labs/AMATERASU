output "instance_profile_name" {
  description = "作成されたIAMインスタンスプロファイルの名前"
  value       = aws_iam_instance_profile.app_profile.name
}

output "role_arn" {
  description = "作成されたIAMロールのARN"
  value       = aws_iam_role.app_role.arn
}

output "ec2_instance_profile_name" {
  description = "Name of the EC2 instance profile"
  value       = aws_iam_instance_profile.ec2_profile.name
}
