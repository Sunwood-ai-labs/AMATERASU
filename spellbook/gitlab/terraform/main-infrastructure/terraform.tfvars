# terraform.tfvars
aws_region         = "ap-northeast-1"
vpc_id             = "vpc-0021a4e9c7c2641fc"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-0cd355401e0f0c039"
public_subnet_2_id = "subnet-0089842ff56bae96d"
security_group_id  = "sg-0e46c8154501d24e8"
ami_id             = "ami-0d52744d6551d851e"
key_name           = "AMATERASU-terraform-keypair-tokyo-PEM"
domain             = "sunwood-ai-labs.click"

project_name       = "amts-gitlab"
instance_type      = "t3.large"
subdomain          = "amaterasu-gitlab-dev"

env_file_path      = "C:/Prj/AMATERASU/spellbook/gitlab/.env"
setup_script_path  = "C:/Prj/AMATERASU/spellbook/gitlab/terraform/main-infrastructure/scripts/setup_script.sh"
