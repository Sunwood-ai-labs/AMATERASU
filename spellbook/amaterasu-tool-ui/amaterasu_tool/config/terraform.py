"""
Terraform設定の読み込みと生成を行うモジュール
"""
import json
import os
from typing import Dict, Any, List, Union

class TerraformConfig:
    """Terraform設定の管理クラス"""

    @staticmethod
    def load_output_json(base_path: str, output_json_path: str) -> Dict[str, Any]:
        """
        output.jsonファイルを読み込む

        Args:
            base_path (str): ベースディレクトリのパス
            output_json_path (str): output.jsonへのパス（ベースパスからの相対パス）

        Returns:
            Dict[str, Any]: 設定値
        """
        full_path = os.path.join(base_path, output_json_path)
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ output.jsonの読み込みに失敗しました: {str(e)}")
            return {}

    @staticmethod
    def get_output_value(outputs: Dict[str, Any], key: str, default: Union[str, List[str]] = "") -> Union[str, List[str]]:
        """
        output.jsonから特定のキーの値を取得

        Args:
            outputs (Dict[str, Any]): output.jsonの内容
            key (str): 取得したい値のキー
            default (Union[str, List[str]]): デフォルト値

        Returns:
            Union[str, List[str]]: 設定値
        """
        try:
            if key in outputs and isinstance(outputs[key], dict):
                return outputs[key].get("value", default)
            return default
        except Exception as e:
            print(f"⚠️ 値の取得に失敗しました（{key}）: {str(e)}")
            return default

    @staticmethod
    def generate_tfvars_content(
        project_name: str,
        project_prefix: str,
        output_json: Dict[str, Any],
        aws_region: str,
        instance_type: str,
        ami_id: str,
        key_name: str
    ) -> str:
        """
        terraform.tfvarsファイルの内容を生成

        Args:
            project_name (str): プロジェクト名
            output_json (Dict[str, Any]): output.jsonの内容
            aws_region (str): AWSリージョン
            instance_type (str): インスタンスタイプ
            ami_id (str): AMI ID
            key_name (str): キーペア名

        Returns:
            str: 生成された内容
        """
        config = TerraformConfig()

        # サブネットIDの取得
        public_subnet_ids = config.get_output_value(output_json, 'public_subnet_ids', ['subnet-default-1', 'subnet-default-2'])
        if isinstance(public_subnet_ids, list) and len(public_subnet_ids) >= 2:
            public_subnet_id = public_subnet_ids[0]
            public_subnet_2_id = public_subnet_ids[1]
        else:
            public_subnet_id = 'subnet-default-1'
            public_subnet_2_id = 'subnet-default-2'

        return f'''# 環境固有のパラメータ
aws_region         = "{aws_region}"
vpc_id             = "{config.get_output_value(output_json, 'vpc_id')}"  # 既存のVPC ID
vpc_cidr           = "{config.get_output_value(output_json, 'vpc_cidr')}"
public_subnet_id   = "{public_subnet_id}"  # 第1パブリックサブネット
public_subnet_2_id = "{public_subnet_2_id}"  # 第2パブリックサブネット

# セキュリティグループID
security_group_ids = [
    "{config.get_output_value(output_json, 'default_security_group_id')}",   # デフォルトセキュリティグループ
    "{config.get_output_value(output_json, 'cloudfront_security_group_id')}", # CloudFrontセキュリティグループ
    "{config.get_output_value(output_json, 'vpc_internal_security_group_id')}", # VPC内部通信用セキュリティグループ
    "{config.get_output_value(output_json, 'whitelist_security_group_id')}"   # ホワイトリストセキュリティグループ
]

# ドメイン設定
domain_internal    = "{config.get_output_value(output_json, 'route53_internal_zone_name')}"  # 内部ドメイン
route53_internal_zone_id = "{config.get_output_value(output_json, 'route53_internal_zone_id')}"  # 内部ゾーンID
subdomain          = "{project_name.replace('amts-', project_prefix)}"

# プロジェクト設定パラメータ
project_name       = "{project_prefix}{project_name}"
instance_type      = "{instance_type}"
ami_id             = "{ami_id}"
key_name           = "{key_name}"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"'''
    
    @staticmethod
    def generate_cloudfront_tfvars_content(
        project_name: str,
        project_prefix: str,
        output_json: Dict[str, Any],
        aws_region: str,
    ) -> str:
        """
        cloudfront terraform.tfvarsファイルの内容を生成

        Args:
            project_name (str): プロジェクト名
            output_json (Dict[str, Any]): output.jsonの内容
            aws_region (str): AWSリージョン

        Returns:
            str: 生成された内容
        """
        config = TerraformConfig()
        
        # ドメイン設定
        domain = config.get_output_value(output_json, 'route53_zone_name')
        subdomain = f"{project_name.replace('amts-', project_prefix)}"

        # オリジンサーバー設定（EC2インスタンス）
        origin_domain = config.get_output_value(output_json, 'ec2_public_ip')

        content = f'''# AWSの設定
aws_region = "{aws_region}"

# プロジェクト名
project_name = "{project_prefix}{project_name}"

# オリジンサーバー設定（EC2インスタンス）
origin_domain = "{origin_domain}"

# ドメイン設定
domain    = "{domain}"
subdomain = "{subdomain}"
'''
        
        cloudfront_tfvars_path = ProjectDiscovery.get_cloudfront_tfvars_path(
            base_path="/home/maki/prj/AMATERASU/spellbook", # TODO: base_path を引数で受け取るように修正
            project_name=project_name
        )
        
        if os.path.exists(cloudfront_tfvars_path):
            # ファイルが既に存在する場合は origin_domain をスキップ
            content_lines = content.splitlines()
            content = "\n".join([line for line in content_lines if "origin_domain" not in line])

        return content
