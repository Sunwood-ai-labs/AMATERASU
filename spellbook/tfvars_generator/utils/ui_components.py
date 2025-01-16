"""
UIコンポーネントを提供するモジュール
"""
import streamlit as st
from typing import Dict, Any, List
from config.project_values import ProjectValues

def show_project_settings_form(project: Dict[str, Any], index: int) -> Dict[str, str]:
    """
    プロジェクトごとの設定フォームを表示
    
    Args:
        project (Dict[str, Any]): プロジェクト情報
        index (int): プロジェクトのインデックス
    
    Returns:
        Dict[str, str]: フォームの入力値
    """
    project_values = ProjectValues(project['path'])
    
    with st.expander(f"🛠️ {project['name']}の設定", expanded=True):
        # 2カラムレイアウト
        col1, col2 = st.columns(2)
        
        with col1:
            # プロジェクト基本設定
            subdomain = st.text_input(
                "サブドメイン",
                key=f"subdomain_{index}",
                value=project_values.get_value('subdomain'),
                help="例: app1, api2 など",
                placeholder="サブドメインを入力"
            )
            
            project_name = st.text_input(
                "プロジェクト名",
                key=f"project_name_{index}",
                value=project_values.get_value('project_name'),
                help="例: web-service, api-server など",
                placeholder="プロジェクト名を入力"
            )
        
        with col2:
            # インスタンス設定
            instance_type = st.selectbox(
                "インスタンスタイプ",
                key=f"instance_type_{index}",
                options=[
                    't3.micro',
                    't3.small',
                    't3.medium',
                    't3.large',
                    't3.xlarge'
                ],
                index=0 if project_values.get_value('instance_type') == '' else 
                        [
                            't3.micro',
                            't3.small',
                            't3.medium',
                            't3.large',
                            't3.xlarge'
                        ].index(project_values.get_value('instance_type'))
            )
            
            ami_id = st.text_input(
                "AMI ID",
                key=f"ami_id_{index}",
                value=project_values.get_value('ami_id'),
                help="例: ami-0bba69335379e17f8",
                placeholder="AMI IDを入力"
            )
            
            key_name = st.text_input(
                "SSH キー名",
                key=f"key_name_{index}",
                value=project_values.get_value('key_name'),
                help="例: my-key-pair",
                placeholder="SSH キー名を入力"
            )
        
        # 設定プレビュー
        if st.checkbox("⚡ 設定内容をプレビュー", key=f"preview_{index}"):
            st.code(f'''
# Project Settings
project_name = "{project_name}"
subdomain    = "{subdomain}"

# Instance Settings
instance_type = "{instance_type}"
ami_id       = "{ami_id}"
key_name     = "{key_name}"
''', language="hcl")
        
        return {
            'subdomain': subdomain,
            'project_name': project_name,
            'instance_type': instance_type,
            'ami_id': ami_id,
            'key_name': key_name
        }

def show_progress_bar(
    current: int,
    total: int,
    prefix: str = "",
    suffix: str = ""
) -> None:
    """
