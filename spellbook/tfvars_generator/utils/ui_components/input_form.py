"""
入力フォームのUIコンポーネントを提供するモジュール
"""
import streamlit as st
from config.project_values import ProjectValues

def show_project_settings(project):
    """
    プロジェクトごとの設定フォームを表示

    Args:
        project (dict): プロジェクト情報
    
    Returns:
        dict: 更新された設定値
    """
    # 既存の設定値を読み込み
    values = ProjectValues(project['path'])
    
    with st.expander(f"📁 {project['name']} の設定", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            subdomain = st.text_input(
                "サブドメイン",
                value=values.get_value('subdomain'),
                key=f"{project['name']}_subdomain",
                help="例: app"
            )
            
            project_name = st.text_input(
                "プロジェクト名",
                value=values.get_value('project_name'),
                key=f"{project['name']}_project_name",
                help="例: myapp"
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
    st.divider()
    st.subheader("⚙️ 設定")
    
    with st.form("tfvars_form"):
        # ドメイン名入力
        domain_name = st.text_input(
            "共通ドメイン名",
            value="sunwood-ai-labs",
            help="例: sunwood-ai-labs",
            placeholder="ドメイン名を入力してください"
        )
        
        # プロジェクトごとの設定
        st.divider()
        st.subheader("🛠️ プロジェクト個別設定")
        project_settings = {}
        for project in projects:
            project_settings[project['name']] = show_project_settings(project)
        
        # 生成ボタン
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
