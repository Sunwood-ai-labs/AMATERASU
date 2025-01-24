"""
プロジェクト固有の設定を管理するモジュール
"""
import os
import re
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    """プロジェクトの設定を管理するモデル"""
    
    subdomain: str = Field(
        default="",
        description="サブドメイン (例: app1, api2)"
    )
    project_name: str = Field(
        default="",
        description="プロジェクト名 (例: web-service, api-server)"
    )
    instance_type: str = Field(
        default="t3.micro",
        description="EC2インスタンスタイプ"
    )
    ami_id: str = Field(
        default="ami-0bba69335379e17f8",
        description="AMI ID"
    )
    key_name: str = Field(
        default="",
        description="SSH キーペア名"
    )

    @classmethod
    def from_tfvars(cls, tfvars_path: str) -> "ProjectConfig":
        """
        terraform.tfvarsファイルから設定を読み込む

        Args:
            tfvars_path (str): terraform.tfvarsファイルのパス

        Returns:
            ProjectConfig: 設定オブジェクト
        """
        values = {
            'subdomain': '',
            'project_name': '',
            'instance_type': 't3.micro',
            'ami_id': 'ami-0bba69335379e17f8',
            'key_name': ''
        }

        if os.path.exists(tfvars_path):
            with open(tfvars_path, 'r') as f:
                content = f.read()
                
                patterns = {
                    'subdomain': r'subdomain\s*=\s*"([^"]*)"',
                    'project_name': r'project_name\s*=\s*"([^"]*)"',
                    'instance_type': r'instance_type\s*=\s*"([^"]*)"',
                    'ami_id': r'ami_id\s*=\s*"([^"]*)"',
                    'key_name': r'key_name\s*=\s*"([^"]*)"'
                }
                
                for key, pattern in patterns.items():
                    match = re.search(pattern, content)
                    if match:
                        values[key] = match.group(1)

        return cls(**values)

    def to_tfvars_content(self) -> str:
        """
        terraform.tfvarsファイルの内容を生成

        Returns:
            str: 生成された内容
        """
        return f'''
# Project Settings
project_name = "{self.project_name}"
subdomain    = "{self.subdomain}"

# Instance Settings
instance_type = "{self.instance_type}"
ami_id       = "{self.ami_id}"
key_name     = "{self.key_name}"'''

    def update(self, new_values: Dict[str, str]) -> None:
        """
        設定値を更新

        Args:
            new_values (Dict[str, str]): 新しい設定値
        """
        for key, value in new_values.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save_to_tfvars(self, tfvars_path: str) -> None:
        """
        設定をterraform.tfvarsファイルに保存

        Args:
            tfvars_path (str): 保存先のパス
        """
        content = self.to_tfvars_content()
        os.makedirs(os.path.dirname(tfvars_path), exist_ok=True)
        
        with open(tfvars_path, 'w') as f:
            f.write(content)
