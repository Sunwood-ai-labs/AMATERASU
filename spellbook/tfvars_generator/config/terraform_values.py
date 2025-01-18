"""
Terraform変数の設定値を管理するモジュール
各値の説明と更新頻度を明記
"""
import os
import json
from typing import Dict, Any, List

def _read_output_json() -> Dict[str, Any]:
    """
    base-infrastructure/output.jsonファイルを読み込む
    
    Returns:
        Dict[str, Any]: output.jsonの内容
    """
    output_path = os.path.join("..", "base-infrastructure", "output.json")
    try:
        with open(output_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading output.json: {str(e)}")
        return {}

def _get_output_value(outputs: Dict[str, Any], key: str) -> Any:
    """
    output.jsonから特定のキーの値を取得
    
    Args:
        outputs (Dict[str, Any]): output.jsonの内容
        key (str): 取得したい値のキー
        
    Returns:
        Any: キーに対応する値
    """
    if key in outputs:
        return outputs[key].get("value")
    return None

def get_terraform_values() -> Dict[str, Any]:
    """
    output.jsonから最新の設定値を取得
    
    Returns:
        Dict[str, Any]: 設定値の辞書
    """
    outputs = _read_output_json()
    
    return {
        "SECURITY_GROUPS": {
            "cloudfront": _get_output_value(outputs, "cloudfront_security_group_id"),
            "default": _get_output_value(outputs, "default_security_group_id"),
            "vpc_internal": _get_output_value(outputs, "vpc_internal_security_group_id"),
            "whitelist": _get_output_value(outputs, "whitelist_security_group_id")
        },
        "SUBNETS": {
            "private": _get_output_value(outputs, "private_subnet_ids"),
            "public": _get_output_value(outputs, "public_subnet_ids")
        },
        "NETWORK": {
            "vpc_id": _get_output_value(outputs, "vpc_id"),
            "vpc_cidr": _get_output_value(outputs, "vpc_cidr"),
            "public_subnet_cidrs": _get_output_value(outputs, "public_subnet_cidrs")
        },
        "ROUTE53": {
            "zone_id": _get_output_value(outputs, "route53_zone_id"),
            "zone_name": _get_output_value(outputs, "route53_zone_name"),
            "internal_zone_id": _get_output_value(outputs, "route53_internal_zone_id"),
            "internal_zone_name": _get_output_value(outputs, "route53_internal_zone_name")
        }
    }

def generate_tfvars_content(project_values: Dict[str, str]) -> str:
    """
    Terraform変数ファイルの内容を生成
    
    Args:
        project_values (Dict[str, str]): プロジェクト固有の設定値
    
    Returns:
        str: terraform.tfvarsファイルの内容
    """
    # 最新の設定値を取得
    values = get_terraform_values()
    
    return f'''# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "{values["NETWORK"]["vpc_id"]}"  # 既存のVPC ID
vpc_cidr           = "{values["NETWORK"]["vpc_cidr"]}"
public_subnet_id   = "{values["SUBNETS"]["public"][0]}"  # 第1パブリックサブネット
public_subnet_2_id = "{values["SUBNETS"]["public"][1]}"  # 第2パブリックサブネット

# セキュリティグループID
security_group_ids = [
    "{values["SECURITY_GROUPS"]["default"]}",   # デフォルトセキュリティグループ
    "{values["SECURITY_GROUPS"]["cloudfront"]}", # CloudFrontセキュリティグループ
    "{values["SECURITY_GROUPS"]["vpc_internal"]}", # VPC内部通信用セキュリティグループ
    "{values["SECURITY_GROUPS"]["whitelist"]}"   # ホワイトリストセキュリティグループ
]

# ドメイン設定
domain_internal    = "{values["ROUTE53"]["internal_zone_name"]}"  # 内部ドメイン
route53_internal_zone_id = "{values["ROUTE53"]["internal_zone_id"]}"  # 内部ゾーンID
subdomain          = "{project_values['subdomain']}"

# プロジェクト設定パラメータ
project_name       = "{project_values['project_name']}"
instance_type      = "{project_values['instance_type']}"
ami_id             = "{project_values['ami_id']}"
key_name           = "{project_values['key_name']}"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"
'''
