"""
AmaterasuToolクラスの統合テスト
"""
import os
import pytest
from amaterasu_tool import AmaterasuTool, ProjectConfig, TerraformConfig

def test_amaterasu_find_projects(sample_project_structure, temp_dir):
    """プロジェクト探索機能の統合テスト"""
    tool = AmaterasuTool(temp_dir)
    
    # 通常の探索
    projects = tool.find_projects(require_cloudfront=False)
    assert len(projects) == 1
    assert projects[0].name == "test-project"
    
    # CloudFront必須の探索
    cloudfront_projects = tool.find_projects(require_cloudfront=True)
    assert len(cloudfront_projects) == 1
    assert cloudfront_projects[0].name == "test-project"
    assert cloudfront_projects[0].cloudfront_tfvars_path is not None

def test_amaterasu_project_config_operations(sample_tfvars):
    """プロジェクト設定操作の統合テスト"""
    tool = AmaterasuTool()
    
    # 設定の読み込み
    config = tool.load_project_config(sample_tfvars)
    assert isinstance(config, ProjectConfig)
    assert config.project_name == "test-project"
    assert config.subdomain == "test-app"
    
    # 設定の保存
    new_config = ProjectConfig(
        project_name="new-project",
        subdomain="new-app",
        instance_type="t3.small"
    )
    new_path = sample_tfvars.replace("terraform.tfvars", "new.tfvars")
    tool.save_project_config(new_config, new_path)
    
    # 保存した設定の読み込み
    loaded_config = tool.load_project_config(new_path)
    assert loaded_config.project_name == "new-project"
    assert loaded_config.subdomain == "new-app"
    assert loaded_config.instance_type == "t3.small"

def test_amaterasu_terraform_config_operations(sample_output_json):
    """Terraform設定操作の統合テスト"""
    tool = AmaterasuTool()
    
    # 設定の読み込み
    config = tool.load_terraform_config(sample_output_json)
    assert isinstance(config, TerraformConfig)
    assert config.security_groups.cloudfront == "sg-test-cf"
    assert config.network.vpc_id == "vpc-test"
    assert config.route53.zone_name == "test.example.com"

def test_amaterasu_cache_cleaning(temp_dir):
    """キャッシュクリーニング機能の統合テスト"""
    tool = AmaterasuTool()
    
    # テスト用のTerraformキャッシュファイルを作成
    terraform_dir = os.path.join(temp_dir, ".terraform")
    os.makedirs(terraform_dir)
    
    tfstate_path = os.path.join(temp_dir, "terraform.tfstate")
    open(tfstate_path, 'w').close()
    
    # キャッシュの削除
    result = tool.clean_terraform_cache(os.path.join(temp_dir, "terraform.tfvars"))
    assert result.success
    assert not os.path.exists(terraform_dir)
    assert not os.path.exists(tfstate_path)

def test_amaterasu_version():
    """バージョン情報取得のテスト"""
    tool = AmaterasuTool()
    version = tool.version()
    assert isinstance(version, str)
    assert version == "0.1.0"  # pyproject.tomlで定義したバージョンと一致することを確認

def test_amaterasu_full_workflow(temp_dir, sample_output_json):
    """完全なワークフローの統合テスト"""
    # プロジェクト構造の作成
    project_dir = os.path.join(temp_dir, "test-project")
    terraform_dir = os.path.join(project_dir, "terraform")
    main_infra_dir = os.path.join(terraform_dir, "main-infrastructure")
    os.makedirs(main_infra_dir)
    
    tool = AmaterasuTool(temp_dir)
    
    # 1. プロジェクトの探索
    projects = tool.find_projects()
    assert len(projects) == 1
    project = projects[0]
    
    # 2. Terraform設定の読み込み
    terraform_config = tool.load_terraform_config(sample_output_json)
    
    # 3. プロジェクト設定の作成と保存
    project_config = ProjectConfig(
        project_name="test-project",
        subdomain="test-app",
        instance_type="t3.micro"
    )
    tfvars_path = os.path.join(main_infra_dir, "terraform.tfvars")
    tool.save_project_config(project_config, tfvars_path)
    
    # 4. 保存した設定の読み込みと検証
    loaded_config = tool.load_project_config(tfvars_path)
    assert loaded_config.project_name == project_config.project_name
    assert loaded_config.subdomain == project_config.subdomain
    
    # 5. キャッシュのクリーニング
    result = tool.clean_terraform_cache(tfvars_path)
    assert result.success
