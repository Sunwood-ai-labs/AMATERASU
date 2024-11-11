# terraform.tfvars
aws_region = "ap-northeast-1"
project_name = "amts-open-webui"
environment = "prod"
price_class = "PriceClass_All"
default_ttl = 3600
max_ttl = 86400
min_ttl = 0

tags = {
  Environment = "prod"
  Project     = "amts-open-webui"
  Terraform   = "true"
}

alb_dns_name           = "amts-open-webui-alb-977186521.ap-northeast-1.elb.amazonaws.com"
alb_target_group_arn   = "arn:aws:elasticloadbalancing:ap-northeast-1:498218886114:targetgroup/amts-open-webui-tg/978c390e455d230a"
instance_id            = "i-062f3dd7388a5da8a"
instance_private_ip    = "10.0.1.189"
instance_public_ip     = "52.198.172.139"
vpc_id                 = "vpc-01bc38e39e2eec458"
alb_security_group_id = "sg-0170f4a3b5c6ad486"  # ALBのセキュリティグループID
