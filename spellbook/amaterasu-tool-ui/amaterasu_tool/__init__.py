"""
Amaterasu Tool - AWSインフラストラクチャ設定管理ツール
"""
from .config import ProjectConfig, TerraformConfig
from .utils import FileOperations, FileOperationResult, ProjectDiscovery, TerraformProject

__version__ = "0.1.0"
__author__ = "Sunwood <dev@sunwood.dev>"
__all__ = [
    # Config
    'ProjectConfig',
    'TerraformConfig',
    
    # Utils
    'FileOperations',
    'FileOperationResult',
    'ProjectDiscovery',
    'TerraformProject'
]

class AmaterasuTool:
    """Amaterasu Toolのメインクラス"""
    
    def __init__(self, base_path: str = ".."):
        """
        Args:
            base_path (str): プロジェクト探索を開始するベースディレクトリのパス
        """
        self.project_discovery = ProjectDiscovery(base_path)
        self.file_operations = FileOperations()

    def find_projects(self, require_cloudfront: bool = False) -> list[TerraformProject]:
        """
        Terraformプロジェクトを探索

        Args:
            require_cloudfront (bool): CloudFrontインフラも必要とするかどうか

        Returns:
            list[TerraformProject]: 検出されたプロジェクトのリスト
        """
        if require_cloudfront:
            return self.project_discovery.find_full_infrastructure_projects()
        return self.project_discovery.find_main_infrastructure_projects()

    def load_project_config(self, tfvars_path: str) -> ProjectConfig:
        """
        プロジェクトの設定を読み込む

        Args:
            tfvars_path (str): terraform.tfvarsファイルのパス

        Returns:
            ProjectConfig: 設定オブジェクト
        """
        return ProjectConfig.from_tfvars(tfvars_path)

    def load_terraform_config(self, output_path: str) -> TerraformConfig:
        """
        Terraformの設定を読み込む

        Args:
            output_path (str): output.jsonファイルのパス

        Returns:
            TerraformConfig: 設定オブジェクト
        """
        return TerraformConfig.from_output_json(output_path)

    def save_project_config(
        self,
        config: ProjectConfig,
        tfvars_path: str
    ) -> None:
        """
        プロジェクトの設定を保存

        Args:
            config (ProjectConfig): 保存する設定
            tfvars_path (str): 保存先のパス
        """
        config.save_to_tfvars(tfvars_path)

    def clean_terraform_cache(self, project_path: str) -> FileOperationResult:
        """
        Terraformのキャッシュを削除

        Args:
            project_path (str): terraform.tfvarsファイルのパス

        Returns:
            FileOperationResult: 削除操作の結果
        """
        return self.file_operations.delete_terraform_cache(project_path)

    @classmethod
    def version(cls) -> str:
        """
        バージョン情報を取得

        Returns:
            str: バージョン文字列
        """
        return __version__
