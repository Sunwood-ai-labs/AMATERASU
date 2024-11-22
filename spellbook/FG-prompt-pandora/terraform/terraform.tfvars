aws_region      = "ap-northeast-1"
project_name    = "prompt-pandora"

vpc_id             = "vpc-0021a4e9c7c2641fc"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-0cd355401e0f0c039"
public_subnet_2_id = "subnet-0089842ff56bae96d"
security_group_id  = "sg-0e46c8154501d24e8"
ami_id             = "ami-0d52744d6551d851e"

container_image = "498218886114.dkr.ecr.ap-northeast-1.amazonaws.com/prompt-pandora:latest"
task_cpu        = "256"
task_memory     = "512"
app_count       = 1

key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain             = "sunwood-ai-labs.click"
subdomain          = "amaterasu-prompt-pandora-dev"
