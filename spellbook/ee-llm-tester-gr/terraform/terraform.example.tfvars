aws_region      = "ap-northeast-1"
project_name    = "amts-ee-llm-tester-gr"

vpc_id             = "vpc-02f238431c68567d5"
vpc_cidr           = "10.0.0.0/16"
public_subnet_id   = "subnet-04a625ee827f37b6a"
public_subnet_2_id = "subnet-0cf88123bbdf60cfd"

# セキュリティグループID
security_group_ids = [
    "sg-039f249b028b22787",
    "sg-02971d71e2149978b",
    "sg-0b5b19ba018fdce2e",
    "sg-09595b69cbd642847"
]

# EC2インスタンス設定
ecs_ami_id     = "ami-00dee0b525da780e0"
instance_type  = "t3.small"

# アプリケーション設定
container_image = "498218886114.dkr.ecr.ap-northeast-1.amazonaws.com/amts-ee-llm-tester-gr:latest"
app_count       = 1

# WAF設定
whitelist_csv_path = "../../whitelist-waf.csv"

ec2_key_name = "AMATERASU-terraform-keypair-tokyo-PEM"
