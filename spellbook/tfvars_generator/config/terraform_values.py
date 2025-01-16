"""
Terraform変数の設定値を管理するモジュール
各値の説明と更新頻度を明記
"""

# Security Groups (低頻度更新)
SECURITY_GROUPS = {
    "cloudfront": "sg-03e35cd397ab91b2d",  # CloudFront配信用SG
    "default": "sg-07f88719c48f3c042",     # デフォルトSG
    "vpc_internal": "sg-0097221f0bf87d747", # VPC内部通信用SG
    "whitelist": "sg-0a7a8064abc5c1aee"     # アクセス許可リストSG
}

# Subnets (低頻度更新)
SUBNETS = {
    "private": [
        "subnet-0381f222f24688fec",  # Private Subnet 1
        "subnet-00f1d3e0b3952b6e0"   # Private Subnet 2
    ],
    "public": [
        "subnet-07ccf2ba130266f91",  # Public Subnet 1
        "subnet-035f1861e57534990"   # Public Subnet 2
    ]
}

# Network Settings (低頻度更新)
NETWORK = {
    "vpc_id": "vpc-0fde6326ce23fcb11",
    "vpc_cidr": "10.0.0.0/16",
    "public_subnet_cidrs": [
        "10.0.1.0/24",  # Public Subnet 1 CIDR
        "10.0.2.0/24"   # Public Subnet 2 CIDR
    ]
}

# Route53 Settings (中頻度更新)
ROUTE53 = {
    "zone_id": "Z09420663OVHTMGC9CBAS",
    "internal_zone_id": "Z09366661CLT9PAXECKAS"
}

def generate_tfvars_content(domain_name):
    """
    Terraform変数ファイルの内容を生成
    
    Args:
        domain_name (str): ドメイン名（例: sunwood-ai-labs）
    
    Returns:
        str: terraform.tfvarsファイルの内容
    """
    return f'''# Security Groups
cloudfront_security_group_id = "{SECURITY_GROUPS["cloudfront"]}"
default_security_group_id = "{SECURITY_GROUPS["default"]}"
vpc_internal_security_group_id = "{SECURITY_GROUPS["vpc_internal"]}"
whitelist_security_group_id = "{SECURITY_GROUPS["whitelist"]}"

# Subnet IDs
private_subnet_ids = [
  "{SUBNETS["private"][0]}",
  "{SUBNETS["private"][1]}",
]
public_subnet_ids = [
  "{SUBNETS["public"][0]}",
  "{SUBNETS["public"][1]}",
]

# Network Settings
vpc_id = "{NETWORK["vpc_id"]}"
vpc_cidr = "{NETWORK["vpc_cidr"]}"
public_subnet_cidrs = tolist([
  "{NETWORK["public_subnet_cidrs"][0]}",
  "{NETWORK["public_subnet_cidrs"][1]}",
])

# Route53 Settings
route53_zone_id = "{ROUTE53["zone_id"]}"
route53_zone_name = "{domain_name}.com"
route53_internal_zone_id = "{ROUTE53["internal_zone_id"]}"
route53_internal_zone_name = "{domain_name}-internal.com"
'''
