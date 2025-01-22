"""
Terraform変数の設定値を管理するモジュール
各値の説明と更新頻度を明記
"""
import os
import json
import streamlit as st
from typing import Dict, Any, List

def _read_output_json() -> Dict[str, Any]:
    """
    base-infrastructure/output.jsonファイルを読み込む
    
    Returns:
        Dict[str, Any]: output.jsonの内容。ファイルが存在しない場合はデフォルト値を含む辞書
    """
    output_path = os.path.join("..", "base-infrastructure", "output.json")
    default_values = {
        "cloudfront_security_group_id": "sg-default-cf",
        "default_security_group_id": "sg-default",
        "vpc_internal_security_group_id": "sg-default-internal",
        "whitelist_security_group_id": "sg-default-whitelist",
        "private_subnet_ids": ["subnet-private-1", "subnet-private-2"],
        "public_subnet_ids": ["subnet-public-1", "subnet-public-2"],
        "vpc_id": "vpc-default",
        "vpc_cidr": "10.0.0.0/16",
        "public_subnet_cidrs": ["10.0.1.0/24", "10.0.2.0/24"],
        "route53_zone_id": "ZONE123456789",
        "route53_zone_name": "example.com",
        "route53_internal_zone_id": "ZONE987654321",
        "route53_internal_zone_name": "internal.example.com"
    }

    try:
        with open(output_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ base-infrastructure/output.jsonが見つかりません。デフォルト値を使用します: {str(e)}")
        return default_values

def _get_output_value(outputs: Dict[str, Any], key: str) -> Any:
    """
    output.jsonから特定のキーの値を取得
    
    Args:
        outputs (Dict[str, Any]): output.jsonの内容
        key (str): 取得したい値のキー
        
    Returns:
        Any: キーに対応する値。値が取得できない場合はNone
    """
    try:
        if isinstance(outputs, dict) and key in outputs:
            value = outputs.get(key)
            if isinstance(value, dict):
                return value.get("value")
            return value
        return None
    except Exception as e:
        st.warning(f"⚠️ 値の取得に失敗しました（{key}）: {str(e)}")
        return None

def get_terraform_values() -> Dict[str, Any]:
    """
    output.jsonから最新の設定値を取得
    値が取得できない場合はデフォルト値を使用
    
    Returns:
        Dict[str, Any]: 設定値の辞書
    """
    outputs = _read_output_json()
    default_values = {
        "SECURITY_GROUPS": {
            "cloudfront": "sg-default-cf",
            "default": "sg-default",
            "vpc_internal": "sg-default-internal",
            "whitelist": "sg-default-whitelist"
        },
        "SUBNETS": {
            "private": ["subnet-private-1", "subnet-private-2"],
            "public": ["subnet-public-1", "subnet-public-2"]
        },
        "NETWORK": {
            "vpc_id": "vpc-default",
            "vpc_cidr": "10.0.0.0/16",
            "public_subnet_cidrs": ["10.0.1.0/24", "10.0.2.0/24"]
        },
        "ROUTE53": {
            "zone_id": "ZONE123456789",
            "zone_name": "example.com",
            "internal_zone_id": "ZONE987654321",
            "internal_zone_name": "internal.example.com"
        }
    }

    try:
        return {
            "SECURITY_GROUPS": {
                "cloudfront": _get_output_value(outputs, "cloudfront_security_group_id") or default_values["SECURITY_GROUPS"]["cloudfront"],
                "default": _get_output_value(outputs, "default_security_group_id") or default_values["SECURITY_GROUPS"]["default"],
                "vpc_internal": _get_output_value(outputs, "vpc_internal_security_group_id") or default_values["SECURITY_GROUPS"]["vpc_internal"],
                "whitelist": _get_output_value(outputs, "whitelist_security_group_id") or default_values["SECURITY_GROUPS"]["whitelist"]
            },
            "SUBNETS": {
                "private": _get_output_value(outputs, "private_subnet_ids") or default_values["SUBNETS"]["private"],
                "public": _get_output_value(outputs, "public_subnet_ids") or default_values["SUBNETS"]["public"]
            },
            "NETWORK": {
                "vpc_id": _get_output_value(outputs, "vpc_id") or default_values["NETWORK"]["vpc_id"],
                "vpc_cidr": _get_output_value(outputs, "vpc_cidr") or default_values["NETWORK"]["vpc_cidr"],
                "public_subnet_cidrs": _get_output_value(outputs, "public_subnet_cidrs") or default_values["NETWORK"]["public_subnet_cidrs"]
            },
            "ROUTE53": {
                "zone_id": _get_output_value(outputs, "route53_zone_id") or default_values["ROUTE53"]["zone_id"],
                "zone_name": _get_output_value(outputs, "route53_zone_name") or default_values["ROUTE53"]["zone_name"],
                "internal_zone_id": _get_output_value(outputs, "route53_internal_zone_id") or default_values["ROUTE53"]["internal_zone_id"],
                "internal_zone_name": _get_output_value(outputs, "route53_internal_zone_name") or default_values["ROUTE53"]["internal_zone_name"]
            }
        }
    except Exception as e:
        st.warning(f"⚠️ 設定値の取得に失敗しました。デフォルト値を使用します: {str(e)}")
        return default_values

def generate_cloudfront_tfvars_content(project_values: Dict[str, str], main_tfvars_path: str) -> str:
    """
    CloudFront用のterraform.tfvarsファイルの内容を生成
    
    Args:
        project_values (Dict[str, str]): プロジェクト固有の設定値
        main_tfvars_path (str): main-infrastructureのterraform.tfvarsファイルのパス
    
    Returns:
        str: terraform.tfvarsファイルの内容
    """
    # 最新の設定値を取得
    values = get_terraform_values()
    
    # main-infrastructureのterraform.tfvarsから情報を読み取る
    origin_domain = ""
    try:
        with open(main_tfvars_path, 'r') as f:
            content = f.read()
            # EC2のパブリックDNSを取得（実行後に設定される想定）
            import re
            match = re.search(r'public_dns\s*=\s*"([^"]*)"', content)
            if match:
                origin_domain = match.group(1)
    except Exception as e:
        st.warning(f"⚠️ main-infrastructureのterraform.tfvarsの読み取りに失敗しました: {str(e)}")
    
    return f'''# AWSの設定
aws_region = "ap-northeast-1"

# プロジェクト名
project_name = "{project_values['project_name']}"

# オリジンサーバー設定（EC2インスタンス）
origin_domain = "{origin_domain}"

# ドメイン設定
domain    = "{values["ROUTE53"]["zone_name"]}"
subdomain = "{project_values['subdomain']}"  # 生成されるURL: {project_values['subdomain']}.{values["ROUTE53"]["zone_name"]}
'''

def generate_main_tfvars_content(project_values: Dict[str, str]) -> str:
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
