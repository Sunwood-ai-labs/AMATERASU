"""
pytest用の共通fixture定義
"""
import os
import pytest
from typing import Generator
from tempfile import TemporaryDirectory
from amaterasu_tool import AmaterasuTool

@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """一時ディレクトリを提供するfixture"""
    with TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_tfvars(temp_dir: str) -> str:
    """サンプルのterraform.tfvarsファイルを提供するfixture"""
    content = '''
# Project Settings
project_name = "test-project"
subdomain    = "test-app"

# Instance Settings
instance_type = "t3.micro"
ami_id       = "ami-0bba69335379e17f8"
key_name     = "test-key"
'''
    tfvars_path = os.path.join(temp_dir, "terraform.tfvars")
    with open(tfvars_path, "w") as f:
        f.write(content)
    return tfvars_path

@pytest.fixture
def sample_output_json(temp_dir: str) -> str:
    """サンプルのoutput.jsonファイルを提供するfixture"""
    content = '''{
    "cloudfront_security_group_id": "sg-test-cf",
    "default_security_group_id": "sg-test",
    "vpc_internal_security_group_id": "sg-test-internal",
    "whitelist_security_group_id": "sg-test-whitelist",
    "private_subnet_ids": ["subnet-private-test-1", "subnet-private-test-2"],
    "public_subnet_ids": ["subnet-public-test-1", "subnet-public-test-2"],
    "vpc_id": "vpc-test",
    "vpc_cidr": "10.0.0.0/16",
    "public_subnet_cidrs": ["10.0.1.0/24", "10.0.2.0/24"],
    "route53_zone_id": "ZONE123TEST",
    "route53_zone_name": "test.example.com",
    "route53_internal_zone_id": "ZONE456TEST",
    "route53_internal_zone_name": "internal.test.example.com"
}'''
    output_path = os.path.join(temp_dir, "output.json")
    with open(output_path, "w") as f:
        f.write(content)
    return output_path

@pytest.fixture
def sample_project_structure(temp_dir: str) -> str:
    """サンプルのプロジェクト構造を提供するfixture"""
    # プロジェクトディレクトリ構造を作成
    project_dir = os.path.join(temp_dir, "test-project")
    terraform_dir = os.path.join(project_dir, "terraform")
    main_infra_dir = os.path.join(terraform_dir, "main-infrastructure")
    cloudfront_infra_dir = os.path.join(terraform_dir, "cloudfront-infrastructure")
    
    # ディレクトリを作成
    os.makedirs(main_infra_dir)
    os.makedirs(cloudfront_infra_dir)
    
    # サンプルファイルを作成
    with open(os.path.join(main_infra_dir, "terraform.tfvars"), "w") as f:
        f.write("# Main infrastructure config")
    
    with open(os.path.join(cloudfront_infra_dir, "terraform.tfvars"), "w") as f:
        f.write("# CloudFront infrastructure config")
    
    return project_dir

@pytest.fixture
def amaterasu() -> AmaterasuTool:
    """AmaterasuToolインスタンスを提供するfixture"""
    return AmaterasuTool()
