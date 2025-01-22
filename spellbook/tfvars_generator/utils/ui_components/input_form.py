"""
入力フォームのUIコンポーネントを提供するモジュール
"""
import streamlit as st
from config.project_values import ProjectValues
from utils.file_operations import delete_terraform_cache

def show_project_settings(project, platform_name, platform_short_name):
    """
    プロジェクトごとの設定フォームを表示

    Args:
        project (dict): プロジェクト情報
        platform_name (str): プラットフォームの正式名称
        platform_short_name (str): プラットフォームの略式名称
    
    Returns:
        dict: 更新された設定値
    """
    values = ProjectValues(project['path'])
    folder_name = project['name'].lower()
    
    with st.expander(f"📁 {project['name']} の設定", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            default_subdomain = f"{platform_name}-{folder_name}" if platform_name else values.get_value('subdomain', '')
            subdomain = st.text_input(
                "サブドメイン",
                value=default_subdomain,
                key=f"{project['name']}_subdomain",
                help="例: amaterasu-coder"
            )
            
            default_project_name = f"{platform_short_name}-{folder_name}" if platform_short_name else values.get_value('project_name', '')
            project_name = st.text_input(
                "プロジェクト名",
                value=default_project_name,
                key=f"{project['name']}_project_name",
                help="例: amts-coder"
            )
            
            instance_type = st.selectbox(
                "インスタンスタイプ",
                options=['t3.micro', 't3.small', 't3.medium', 't3.large'],
                index=['t3.micro', 't3.small', 't3.medium', 't3.large'].index(
                    values.get_value('instance_type', 't3.micro')
                ),
                key=f"{project['name']}_instance_type"
            )
        
        with col2:
            ami_id = st.text_input(
                "AMI ID",
                value=values.get_value('ami_id', 'ami-0bba69335379e17f8'),
                key=f"{project['name']}_ami_id",
                help="例: ami-0bba69335379e17f8"
            )
            
            key_name = st.text_input(
                "キーペア名",
                value=values.get_value('key_name'),
                key=f"{project['name']}_key_name",
                help="例: myapp-key"
            )
        
        return {
            'subdomain': subdomain,
            'project_name': project_name,
            'instance_type': instance_type,
            'ami_id': ami_id,
            'key_name': key_name
        }

def show_input_form(projects, on_generate):
    """
    入力フォームを表示

    Args:
        projects (list): プロジェクト情報のリスト
        on_generate (callable): 生成ボタン押下時のコールバック関数
              引数: (projects, domain_name, project_settings)
    """
    with st.form("tfvars_form"):
        st.subheader("⚙️ 共通設定")
        
        col1, col2 = st.columns(2)
        with col1:
            platform_name = st.text_input(
                "プラットフォーム正式名称",
                value="amaterasu",
                key="platform_name",
                help="例: amaterasu",
                placeholder="正式名称を入力してください"
            )
        
        with col2:
            platform_short_name = st.text_input(
                "プラットフォーム略式名称",
                value="amts",
                key="platform_short_name",
                help="例: amts",
                placeholder="略式名称を入力してください"
            )
            
        domain_name = st.text_input(
            "共通ドメイン名",
            value="sunwood-ai-labs",
            key="tfvars_domain_name",
            help="例: sunwood-ai-labs",
            placeholder="ドメイン名を入力してください"
        )
        
        st.divider()
        st.subheader("🛠️ プロジェクト個別設定")
        project_settings = {}
        for project in projects:
            project_settings[project['name']] = show_project_settings(
                project,
                platform_name,
                platform_short_name
            )
        
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 生成開始",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            if not domain_name:
                st.error("🚫 ドメイン名を入力してください")
                return
                
            if not projects:
                st.error("🚫 対象プロジェクトが見つかりませんでした")
                return
            
            # 生成処理の実行
            on_generate(projects, domain_name, project_settings)
