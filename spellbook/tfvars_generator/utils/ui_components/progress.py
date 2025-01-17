"""
進捗表示のUIコンポーネントを提供するモジュール
"""
import streamlit as st
import time
from config.terraform_values import generate_tfvars_content
from config.project_values import ProjectValues
from utils.file_operations import write_tfvars

def generate_files_with_progress(projects, domain_name, project_settings):
    """
    terraform.tfvarsファイルを生成し、進捗状況を表示

    Args:
        projects (list): プロジェクト情報のリスト
        domain_name (str): ドメイン名
        project_settings (dict): プロジェクトごとの設定値
            {
                'project_name': {
                    'subdomain': str,
                    'project_name': str,
                    'instance_type': str,
                    'ami_id': str,
                    'key_name': str
                }
            }
    """
    st.divider()
    st.subheader("🔄 生成状況")
    
    # プログレスバーで進捗表示
    progress_text = "ファイル生成の進捗状況"
    progress_bar = st.progress(0, text=progress_text)
    
    for i, project in enumerate(projects):
        progress = (i + 1) / len(projects)
        progress_bar.progress(progress, text=f"処理中: {project['name']}")
        
        with st.spinner(f"💾 {project['name']}のファイルを生成中..."):
            # プロジェクト固有の設定を取得
            project_values = project_settings[project['name']]
            
            # terraform.tfvarsの内容を生成
            content = generate_tfvars_content(project_values)
            
            # ファイルに書き込み
            write_tfvars(project, content)
            time.sleep(0.5)  # UIの動きを視覚化するための遅延
    
    st.success("✨ 全てのファイルの生成が完了しました！")
    st.balloons()
