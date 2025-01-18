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
    
    with st.expander("🔄 現在の設定値（base-infrastructure/output.jsonから読み込み）", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔒 セキュリティグループ")
            st.code(f"""
CloudFront: {values['SECURITY_GROUPS']['cloudfront']}
Default: {values['SECURITY_GROUPS']['default']}
VPC Internal: {values['SECURITY_GROUPS']['vpc_internal']}
Whitelist: {values['SECURITY_GROUPS']['whitelist']}
""")
            
            st.markdown("#### 🌐 サブネット")
            st.code(f"""
Private Subnets:
- {values['SUBNETS']['private'][0]}
- {values['SUBNETS']['private'][1]}

Public Subnets:
- {values['SUBNETS']['public'][0]}
- {values['SUBNETS']['public'][1]}
""")
        
        with col2:
            st.markdown("#### 🏢 VPC設定")
            st.code(f"""
VPC ID: {values['NETWORK']['vpc_id']}
VPC CIDR: {values['NETWORK']['vpc_cidr']}

Public Subnet CIDRs:
- {values['NETWORK']['public_subnet_cidrs'][0]}
- {values['NETWORK']['public_subnet_cidrs'][1]}
""")
            
            st.markdown("#### 🔍 Route53設定")
            st.code(f"""
Zone ID: {values['ROUTE53']['zone_id']}
Zone Name: {values['ROUTE53']['zone_name']}
Internal Zone ID: {values['ROUTE53']['internal_zone_id']}
Internal Zone Name: {values['ROUTE53']['internal_zone_name']}
""")

def initialize_page():
    """ページの初期化を行う"""
    set_page_config()
    show_header()
