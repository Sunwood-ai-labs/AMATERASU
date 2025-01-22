"""
Terraform変数ファイルジェネレーター
メインページ
"""
import streamlit as st
from config.terraform_values import get_terraform_values

def show_current_values():
    """現在の設定値を表示"""
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

def main():
    """メイン関数"""
    st.set_page_config(
        page_title="Terraform Vars Generator",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 Terraform Variables Generator")
    st.markdown("""
    ### 📝 概要
    このツールは、Terraformプロジェクトの変数ファイル（terraform.tfvars）を
    効率的に管理するためのWebアプリケーションです。

    ### 🎯 主な機能
    1. 🔄 **変数ファイルの生成** (Generate TFVars)
       - terraform.tfvarsファイルの自動生成
       - プロジェクトの自動検出
       - 共通設定の一括適用
    
    2. 🗑️ **キャッシュ管理** (Cache Manager)
       - 複数プロジェクトの一括選択
       - Terraformキャッシュの安全な削除
       - 処理状況のリアルタイム表示
    """)
    
    st.divider()
    
    # 現在の設定値を表示
    show_current_values()

if __name__ == "__main__":
    main()
