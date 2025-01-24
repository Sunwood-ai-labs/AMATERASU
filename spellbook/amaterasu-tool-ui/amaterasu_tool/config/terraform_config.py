"""
Terraform全体の設定を管理するモジュール
"""
import json
import os
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SecurityGroupConfig(BaseModel):
    """セキュリティグループの設定"""
    cloudfront: str = Field(
        default="sg-default-cf",
        description="CloudFront用セキュリティグループID"
    )
    default: str = Field(
        default="sg-default",
        description="デフォルトセキュリティグループID"
    )
    vpc_internal: str = Field(
        default="sg-default-internal",
        description="VPC内部通信用セキュリティグループID"
    )
    whitelist: str = Field(
        default="sg-default-whitelist",
        description="ホワイトリスト用セキュリティグループID"
    )

class SubnetConfig(BaseModel):
    """サブネットの設定"""
    private: List[str] = Field(
        default=["subnet-private-1", "subnet-private-2"],
        description="プライベートサブネットIDのリスト"
    )
    public: List[str] = Field(
        default=["subnet-public-1", "subnet-public-2"],
        description="パブリックサブネットIDのリスト"
    )

class NetworkConfig(BaseModel):
    """ネットワークの設定"""
    vpc_id: str = Field(
        default="vpc-default",
        description="VPC ID"
    )
    vpc_cidr: str = Field(
        default="10.0.0.0/16",
        description="VPC CIDR"
    )
    public_subnet_cidrs: List[str] = Field(
        default=["10.0.1.0/24", "10.0.2.0/24"],
        description="パブリックサブネットのCIDRリスト"
    )

class Route53Config(BaseModel):
    """Route53の設定"""
    zone_id: str = Field(
        default="ZONE123456789",
        description="Route53 ゾーンID"
    )
    zone_name: str = Field(
        default="example.com",
        description="Route53 ゾーン名"
    )
    internal_zone_id: str = Field(
        default="ZONE987654321",
        description="内部用Route53 ゾーンID"
    )
    internal_zone_name: str = Field(
        default="internal.example.com",
        description="内部用Route53 ゾーン名"
    )

class TerraformConfig(BaseModel):
    """Terraform全体の設定を管理するモデル"""
    security_groups: SecurityGroupConfig = Field(
        default_factory=SecurityGroupConfig,
        description="セキュリティグループの設定"
    )
    subnets: SubnetConfig = Field(
        default_factory=SubnetConfig,
        description="サブネットの設定"
    )
    network: NetworkConfig = Field(
        default_factory=NetworkConfig,
        description="ネットワークの設定"
    )
    route53: Route53Config = Field(
        default_factory=Route53Config,
        description="Route53の設定"
    )

    @classmethod
    def from_output_json(cls, output_path: str) -> "TerraformConfig":
        """
        base-infrastructure/output.jsonから設定を読み込む

        Args:
            output_path (str): output.jsonファイルのパス

        Returns:
            TerraformConfig: 設定オブジェクト
        """
        try:
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            return cls(
                security_groups=SecurityGroupConfig(
                    cloudfront=cls._get_output_value(data, "cloudfront_security_group_id"),
                    default=cls._get_output_value(data, "default_security_group_id"),
                    vpc_internal=cls._get_output_value(data, "vpc_internal_security_group_id"),
                    whitelist=cls._get_output_value(data, "whitelist_security_group_id")
                ),
                subnets=SubnetConfig(
                    private=cls._get_output_value(data, "private_subnet_ids"),
                    public=cls._get_output_value(data, "public_subnet_ids")
                ),
                network=NetworkConfig(
                    vpc_id=cls._get_output_value(data, "vpc_id"),
                    vpc_cidr=cls._get_output_value(data, "vpc_cidr"),
                    public_subnet_cidrs=cls._get_output_value(data, "public_subnet_cidrs")
                ),
                route53=Route53Config(
                    zone_id=cls._get_output_value(data, "route53_zone_id"),
                    zone_name=cls._get_output_value(data, "route53_zone_name"),
                    internal_zone_id=cls._get_output_value(data, "route53_internal_zone_id"),
                    internal_zone_name=cls._get_output_value(data, "route53_internal_zone_name")
                )
            )
        except Exception as e:
            print(f"⚠️ output.jsonの読み込みに失敗しました: {str(e)}")
            return cls()

    @staticmethod
    def _get_output_value(outputs: Dict[str, Any], key: str) -> Any:
        """
        output.jsonから特定のキーの値を取得

        Args:
            outputs (Dict[str, Any]): output.jsonの内容
            key (str): 取得したい値のキー

        Returns:
            Any: キーに対応する値
        """
        try:
            if isinstance(outputs, dict) and key in outputs:
                value = outputs.get(key)
                if isinstance(value, dict):
                    return value.get("value")
                return value
            return None
        except Exception as e:
            print(f"⚠️ 値の取得に失敗しました（{key}）: {str(e)}")
            return None

    def generate_main_tfvars(self, project_config: "ProjectConfig") -> str:
        """
        main-infrastructure用のterraform.tfvars内容を生成

        Args:
            project_config (ProjectConfig): プロジェクト設定

        Returns:
            str: 生成された内容
        """
        return f'''# 環境固有のパラメータ
aws_region         = "ap-northeast-1"
vpc_id             = "{self.network.vpc_id}"
vpc_cidr           = "{self.network.vpc_cidr}"
public_subnet_id   = "{self.subnets.public[0]}"
public_subnet_2_id = "{self.subnets.public[1]}"

# セキュリティグループID
security_group_ids = [
    "{self.security_groups.default}",
    "{self.security_groups.cloudfront}",
    "{self.security_groups.vpc_internal}",
    "{self.security_groups.whitelist}"
]

# ドメイン設定
domain_internal    = "{self.route53.internal_zone_name}"
route53_internal_zone_id = "{self.route53.internal_zone_id}"
subdomain          = "{project_config.subdomain}"

# プロジェクト設定
project_name       = "{project_config.project_name}"
instance_type      = "{project_config.instance_type}"
ami_id             = "{project_config.ami_id}"
key_name           = "{project_config.key_name}"

# ローカルファイルパス
env_file_path      = "../../.env"
setup_script_path  = "./scripts/setup_script.sh"'''

    def generate_cloudfront_tfvars(
        self,
        project_config: "ProjectConfig",
        origin_domain: Optional[str] = None
    ) -> str:
        """
        cloudfront-infrastructure用のterraform.tfvars内容を生成

        Args:
            project_config (ProjectConfig): プロジェクト設定
            origin_domain (Optional[str]): オリジンドメイン

        Returns:
            str: 生成された内容
        """
        return f'''# AWSの設定
aws_region = "ap-northeast-1"

# プロジェクト名
project_name = "{project_config.project_name}"

# オリジンサーバー設定（EC2インスタンス）
origin_domain = "{origin_domain or ''}"

# ドメイン設定
domain    = "{self.route53.zone_name}"
subdomain = "{project_config.subdomain}"  # 生成されるURL: {project_config.subdomain}.{self.route53.zone_name}
'''
