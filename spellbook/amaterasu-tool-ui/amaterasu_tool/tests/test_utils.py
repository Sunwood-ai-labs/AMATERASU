"""
ユーティリティ機能のテスト
"""
import os
import shutil
import pytest
from amaterasu_tool.utils import (
    FileOperations,
    ProjectDiscovery,
    FileOperationResult,
    TerraformProject
)

def test_project_discovery_find_main_infrastructure(sample_project_structure, temp_dir):
    """main-infrastructureプロジェクトの探索機能をテスト"""
    discovery = ProjectDiscovery(temp_dir)
    projects = discovery.find_main_infrastructure_projects()
    
    assert len(projects) == 1
    assert projects[0].name == "test-project"
    assert os.path.basename(projects[0].abs_path) == "test-project"
    assert projects[0].main_tfvars_path.endswith("main-infrastructure/terraform.tfvars")

def test_project_discovery_find_full_infrastructure(sample_project_structure, temp_dir):
    """両方のインフラを持つプロジェクトの探索機能をテスト"""
    discovery = ProjectDiscovery(temp_dir)
    projects = discovery.find_full_infrastructure_projects()
    
    assert len(projects) == 1
    project = projects[0]
    assert project.name == "test-project"
    assert project.main_tfvars_path.endswith("main-infrastructure/terraform.tfvars")
    assert project.cloudfront_tfvars_path.endswith("cloudfront-infrastructure/terraform.tfvars")

def test_project_discovery_empty_directory(temp_dir):
    """空ディレクトリでの探索機能をテスト"""
    discovery = ProjectDiscovery(temp_dir)
    projects = discovery.find_main_infrastructure_projects()
    assert len(projects) == 0

def test_file_operations_write_and_read(temp_dir):
    """ファイルの書き込みと読み込み機能をテスト"""
    ops = FileOperations()
    test_path = os.path.join(temp_dir, "test", "file.txt")
    test_content = "Hello, World!"
    
    # ファイルの書き込み
    ops.write_file(test_path, test_content)
    assert os.path.exists(test_path)
    
    # ファイルの読み込み
    content = ops.read_file(test_path)
    assert content == test_content
    
    # 存在しないファイルの読み込み
    none_content = ops.read_file(os.path.join(temp_dir, "nonexistent.txt"))
    assert none_content is None

def test_terraform_cache_deletion(temp_dir):
    """Terraformキャッシュの削除機能をテスト"""
    # テスト用のTerraformキャッシュファイルを作成
    terraform_dir = os.path.join(temp_dir, ".terraform")
    os.makedirs(terraform_dir)
    
    tfstate_path = os.path.join(temp_dir, "terraform.tfstate")
    tfstate_backup_path = os.path.join(temp_dir, "terraform.tfstate.backup")
    lock_path = os.path.join(temp_dir, ".terraform.lock.hcl")
    
    # ダミーファイルを作成
    open(tfstate_path, 'w').close()
    open(tfstate_backup_path, 'w').close()
    open(lock_path, 'w').close()
    
    ops = FileOperations()
    result = ops.delete_terraform_cache(os.path.join(temp_dir, "terraform.tfvars"))
    
    # 削除結果の検証
    assert result.success
    assert not os.path.exists(terraform_dir)
    assert not os.path.exists(tfstate_path)
    assert not os.path.exists(tfstate_backup_path)
    assert not os.path.exists(lock_path)
    
    # 削除されたアイテムの検証
    deleted_paths = [item.path for item in result.deleted_items]
    assert len(deleted_paths) == 4
    assert terraform_dir in deleted_paths
    assert tfstate_path in deleted_paths
    assert tfstate_backup_path in deleted_paths
    assert lock_path in deleted_paths

def test_terraform_cache_deletion_nonexistent(temp_dir):
    """存在しないキャッシュファイルの削除をテスト"""
    ops = FileOperations()
    result = ops.delete_terraform_cache(os.path.join(temp_dir, "terraform.tfvars"))
    
    assert result.success
    assert len(result.deleted_items) == 0
    assert len(result.skipped_items) == 4  # 全てのファイルがスキップされる

def test_ensure_directory(temp_dir):
    """ディレクトリ作成機能をテスト"""
    ops = FileOperations()
    test_dir = os.path.join(temp_dir, "test", "nested", "directory")
    
    # ディレクトリが存在しない場合は作成される
    ops.ensure_directory(test_dir)
    assert os.path.exists(test_dir)
    assert os.path.isdir(test_dir)
    
    # 既に存在する場合はエラーにならない
    ops.ensure_directory(test_dir)
    assert os.path.exists(test_dir)
