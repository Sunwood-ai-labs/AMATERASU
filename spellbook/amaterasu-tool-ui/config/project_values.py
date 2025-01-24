"""
プロジェクト固有の設定値を管理するモジュール
"""
import os
import re
import configparser
from typing import Dict, Optional

class ProjectValues:
    def __init__(self, tfvars_path: str):
        """
        Args:
            tfvars_path (str): terraform.tfvarsファイルのパス
        """
        self.tfvars_path = tfvars_path
        self.values = self._load_existing_values()

    def _load_existing_values(self) -> Dict[str, str]:
        """既存のtfvarsファイルから値を読み込む"""
        values = {
            'subdomain': '',
            'project_name': '',
            'instance_type': 't3.micro',  # デフォルト値
            'ami_id': 'ami-0bba69335379e17f8',  # デフォルト値
            'key_name': ''
        }
        
        if os.path.exists(self.tfvars_path):
            with open(self.tfvars_path, 'r') as f:
                content = f.read()
                
                # 各値を正規表現で抽出
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
        
        return values

    def get_value(self, key: str, default: str = '') -> str:
        """
        指定されたキーの値を取得
        
        Args:
            key (str): 取得する値のキー
            default (str): デフォルト値
            
        Returns:
            str: 設定値
        """
        return self.values.get(key, default)

    def update_values(self, new_values: Dict[str, str]):
        """
        値を更新
        
        Args:
            new_values (Dict[str, str]): 新しい値
        """
        self.values.update(new_values)

    def generate_project_content(self) -> str:
        """
        プロジェクト固有の設定内容を生成
        
        Returns:
            str: terraform.tfvarsに追加する内容
        """
        return f'''
# Project Settings
project_name = "{self.values['project_name']}"
subdomain = "{self.values['subdomain']}"

# Instance Settings
instance_type = "{self.values['instance_type']}"
ami_id = "{self.values['ami_id']}"
key_name = "{self.values['key_name']}"'''
