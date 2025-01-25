"""
プロジェクト探索機能を提供するモジュール
"""
import os
from typing import List

class ProjectDiscovery:
    """プロジェクト探索クラス"""

    @staticmethod
    def find_projects(base_path: str, project_dir: str = None) -> List[str]:
        """
        Terraformプロジェクトを探索

        Args:
            base_path (str): ベースディレクトリのパス
            project_dir (str, optional): 特定のプロジェクトディレクトリ

        Returns:
            List[str]: プロジェクトディレクトリのリスト
        """
        projects = []
        
        if project_dir:
            # 特定のプロジェクトが指定された場合
            project_path = os.path.join(base_path, project_dir)
            terraform_dir = os.path.join(project_path, "terraform", "main-infrastructure")
            if os.path.exists(terraform_dir):
                projects.append(project_dir)
        else:
            # すべてのプロジェクトを探索
            for item in os.listdir(base_path):
                if os.path.isdir(os.path.join(base_path, item)):
                    terraform_dir = os.path.join(base_path, item, "terraform", "main-infrastructure")
                    if os.path.exists(terraform_dir):
                        projects.append(item)

        return sorted(projects)

    @staticmethod
    def get_tfvars_path(base_path: str, project_name: str) -> str:
        """
        プロジェクトのterraform.tfvarsファイルパスを取得

        Args:
            base_path (str): ベースディレクトリのパス
            project_name (str): プロジェクト名

        Returns:
            str: terraform.tfvarsファイルのパス
        """
        return os.path.join(
            base_path,
            project_name,
            "terraform",
            "main-infrastructure",
            "terraform.tfvars"
        )
