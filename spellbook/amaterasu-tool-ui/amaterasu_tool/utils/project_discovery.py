"""
プロジェクト探索機能を提供するモジュール
"""
import os
import glob
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TerraformProject:
    """Terraformプロジェクトの情報を格納するデータクラス"""
    name: str
    abs_path: str
    main_tfvars_path: Optional[str] = None
    cloudfront_tfvars_path: Optional[str] = None
    output_json_path: Optional[str] = None

class ProjectDiscovery:
    """プロジェクト探索クラス"""

    def __init__(self, base_path: str = ".."):
        """
        Args:
            base_path (str): 探索を開始するベースディレクトリのパス
        """
        self.base_path = os.path.abspath(base_path)

    def find_terraform_projects(self, require_cloudfront: bool = False) -> List[TerraformProject]:
        """
        Terraformプロジェクトを探索

        Args:
            require_cloudfront (bool): CloudFrontインフラも必要とするかどうか

        Returns:
            List[TerraformProject]: 検出されたプロジェクトのリスト
        """
        projects = []
        
        for project_dir in glob.glob(os.path.join(self.base_path, "*/")):
            abs_project_dir = os.path.abspath(project_dir)
            terraform_dir = os.path.join(abs_project_dir, "terraform")
            main_infra_dir = os.path.join(terraform_dir, "main-infrastructure")
            cloudfront_infra_dir = os.path.join(terraform_dir, "cloudfront-infrastructure")

            # main-infrastructureディレクトリの存在確認
            if not os.path.exists(main_infra_dir):
                continue

            project_name = os.path.basename(abs_project_dir)
            if not project_name or project_name == "terraform":
                continue

            # CloudFrontの要件チェック
            if require_cloudfront and not os.path.exists(cloudfront_infra_dir):
                continue

            project = TerraformProject(
                name=project_name,
                abs_path=abs_project_dir,
                main_tfvars_path=os.path.join(main_infra_dir, "terraform.tfvars"),
                output_json_path=os.path.join(main_infra_dir, "output.json")
            )

            # CloudFrontパスの設定
            if os.path.exists(cloudfront_infra_dir):
                project.cloudfront_tfvars_path = os.path.join(
                    cloudfront_infra_dir,
                    "terraform.tfvars"
                )

            projects.append(project)

        # プロジェクト名でソート
        projects.sort(key=lambda x: x.name)
        return projects

    def find_main_infrastructure_projects(self) -> List[TerraformProject]:
        """
        main-infrastructureを持つプロジェクトのみを探索

        Returns:
            List[TerraformProject]: 検出されたプロジェクトのリスト
        """
        return self.find_terraform_projects(require_cloudfront=False)

    def find_full_infrastructure_projects(self) -> List[TerraformProject]:
        """
        main-infrastructureとcloudfront-infrastructureの両方を持つ
        プロジェクトを探索

        Returns:
            List[TerraformProject]: 検出されたプロジェクトのリスト
        """
        return self.find_terraform_projects(require_cloudfront=True)
