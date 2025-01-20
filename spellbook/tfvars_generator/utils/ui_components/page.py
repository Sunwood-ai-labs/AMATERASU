"""
ページ設定とヘッダー関連のUIコンポーネントを提供するモジュール
"""
import streamlit as st

def set_page_config():
    """ページの初期設定を行う"""
    from .styles import get_style_definitions

    st.set_page_config(
        page_title="Terraform Vars Generator",
        page_icon="🎮",
        layout="wide"
    )
    
    # モダンなテーマカラーを設定
    st.markdown(get_style_definitions(), unsafe_allow_html=True)

def show_header():
    """ヘッダーを表示"""
    from config.terraform_values import get_terraform_values

    st.title("🎮 Terraform Variables Generator")
    st.markdown("""
    ### 概要
    このツールは、`terraform/main-infrastructure`ディレクトリを持つ
    プロジェクトに対して、`terraform.tfvars`ファイルを自動生成します。
    """)

    # 現在の設定値を取得して表示
    values = get_terraform_values()
    
    with st.expander("🔄 現在の設定値", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔒 セキュリティグループ")
            if values.get('SECURITY_GROUPS'):
                st.code(f"""
CloudFront: {values['SECURITY_GROUPS'].get('cloudfront', 'N/A')}
Default: {values['SECURITY_GROUPS'].get('default', 'N/A')}
VPC Internal: {values['SECURITY_GROUPS'].get('vpc_internal', 'N/A')}
Whitelist: {values['SECURITY_GROUPS'].get('whitelist', 'N/A')}
""")
            
            st.markdown("#### 🌐 サブネット")
            if values.get('SUBNETS'):
                private_subnets = values['SUBNETS'].get('private', ['N/A', 'N/A'])
                public_subnets = values['SUBNETS'].get('public', ['N/A', 'N/A'])
                st.code(f"""
Private Subnets:
- {private_subnets[0] if len(private_subnets) > 0 else 'N/A'}
- {private_subnets[1] if len(private_subnets) > 1 else 'N/A'}

Public Subnets:
- {public_subnets[0] if len(public_subnets) > 0 else 'N/A'}
- {public_subnets[1] if len(public_subnets) > 1 else 'N/A'}
""")
        
        with col2:
            st.markdown("#### 🏢 VPC設定")
            if values.get('NETWORK'):
                subnet_cidrs = values['NETWORK'].get('public_subnet_cidrs', ['N/A', 'N/A'])
                st.code(f"""
VPC ID: {values['NETWORK'].get('vpc_id', 'N/A')}
VPC CIDR: {values['NETWORK'].get('vpc_cidr', 'N/A')}

Public Subnet CIDRs:
- {subnet_cidrs[0] if len(subnet_cidrs) > 0 else 'N/A'}
- {subnet_cidrs[1] if len(subnet_cidrs) > 1 else 'N/A'}
""")
            
            st.markdown("#### 🔍 Route53設定")
            if values.get('ROUTE53'):
                st.code(f"""
Zone ID: {values['ROUTE53'].get('zone_id', 'N/A')}
Zone Name: {values['ROUTE53'].get('zone_name', 'N/A')}
Internal Zone ID: {values['ROUTE53'].get('internal_zone_id', 'N/A')}
Internal Zone Name: {values['ROUTE53'].get('internal_zone_name', 'N/A')}
""")

def initialize_page():
    """ページの初期化を行う"""
    set_page_config()
    show_header()
