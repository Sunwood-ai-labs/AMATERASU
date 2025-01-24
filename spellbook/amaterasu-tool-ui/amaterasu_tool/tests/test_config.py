"""
設定管理機能のテスト
"""
import os
import pytest
from amaterasu_tool import ProjectConfig, TerraformConfig

def test_project_config_from_tfvars(sample_tfvars):
    """ProjectConfigがterraform.tfvarsから正しく設定を読み込めることをテスト"""
    config = ProjectConfig.from_tfvars(sample_tfvars)
    
    assert config.project_name == "test-project"
    assert config.subdomain == "test-app"
    assert config.instance_type == "t3.micro"
    assert config.ami_id == "ami-0bba69335379e17f8"
    assert config.key_name == "test-key"

def test_project_config_save(temp_dir):
    """ProjectConfigが正しく設定を保存できることをテスト"""
    config = ProjectConfig(
        project_name="test-project",
        subdomain="test-app",
        instance_type="t3.micro",
        ami_id="ami-test",
        key_name="test-key"
    )
    
    save_path = os.path.join(temp_dir, "new.tfvars")
    config.save_to_tfvars(save_path)
    
    # 保存した設定を読み込んで検証
    loaded_config = ProjectConfig.from_tfvars(save_path)
    assert loaded_config.project_name == config.project_name
    assert loaded_config.subdomain == config.subdomain
    assert loaded_config.instance_type == config.instance_type
    assert loaded_config.ami_id == config.ami_id
    assert loaded_config.key_name == config.key_name

def test_terraform_config_from_output_json(sample_output_json):
    """TerraformConfigがoutput.jsonから正しく設定を読み込めることをテスト"""
    config = TerraformConfig.from_output_json(sample_output_json)
    
    # セキュリティグループ設定の検証
    assert config.security_groups.cloudfront == "sg-test-cf"
    assert config.security_groups.default == "sg-test"
    assert config.security_groups.vpc_internal == "sg-test-internal"
    assert config.security_groups.whitelist == "sg-test-whitelist"
    
    # サブネット設定の検証
    assert config.subnets.private == ["subnet-private-test-1", "subnet-private-test-2"]
    assert config.subnets.public == ["subnet-public-test-1", "subnet-public-test-2"]
    
    # ネットワーク設定の検証
    assert config.network.vpc_id == "vpc-test"
    assert config.network.vpc_cidr == "10.0.0.0/16"
    assert config.network.public_subnet_cidrs == ["10.0.1.0/24", "10.0.2.0/24"]
    
    # Route53設定の検証
    assert config.route53.zone_id == "ZONE123TEST"
    assert config.route53.zone_name == "test.example.com"
    assert config.route53.internal_zone_id == "ZONE456TEST"
    assert config.route53.internal_zone_name == "internal.test.example.com"

def test_terraform_config_generate_main_tfvars():
    """TerraformConfigがmain-infrastructure用の設定を正しく生成できることをテスト"""
    terraform_config = TerraformConfig()
    project_config = ProjectConfig(
        project_name="test-project",
        subdomain="test-app",
        instance_type="t3.micro",
        ami_id="ami-test",
        key_name="test-key"
    )
    
    content = terraform_config.generate_main_tfvars(project_config)
    
    # 生成された内容に必要な設定が含まれていることを検証
    assert "aws_region" in content
    assert 'project_name = "test-project"' in content
    assert 'subdomain = "test-app"' in content
    assert 'instance_type = "t3.micro"' in content
    assert 'ami_id = "ami-test"' in content
    assert 'key_name = "test-key"' in content

def test_terraform_config_generate_cloudfront_tfvars():
    """TerraformConfigがcloudfront-infrastructure用の設定を正しく生成できることをテスト"""
    terraform_config = TerraformConfig()
    project_config = ProjectConfig(
        project_name="test-project",
        subdomain="test-app"
    )
    
    content = terraform_config.generate_cloudfront_tfvars(
        project_config,
        origin_domain="test.example.com"
    )
    
    # 生成された内容に必要な設定が含まれていることを検証
    assert "aws_region" in content
    assert 'project_name = "test-project"' in content
    assert 'subdomain = "test-app"' in content
    assert 'origin_domain = "test.example.com"' in content

def test_project_config_update():
    """ProjectConfigが設定を正しく更新できることをテスト"""
    config = ProjectConfig(
        project_name="old-project",
        subdomain="old-app"
    )
    
    config.update({
        "project_name": "new-project",
        "subdomain": "new-app"
    })
    
    assert config.project_name == "new-project"
    assert config.subdomain == "new-app"
