"""
ファイル操作に関するユーティリティ関数を提供するモジュール
"""
import os
import streamlit as st

def create_directory_if_not_exists(path):
    """
    指定されたパスにディレクトリが存在しない場合、ディレクトリを作成

    Args:
        path (str): 作成するディレクトリのパス
    """
    if not os.path.exists(path):
        os.makedirs(path)

def write_tfvars(project, content):
    """
    指定されたプロジェクトのterraform.tfvarsファイルを生成

    Args:
        project (dict): プロジェクト情報 (name, pathを含む)
        content (str): terraform.tfvarsファイルの内容
    """
    dir_path = os.path.dirname(project['path'])
    create_directory_if_not_exists(dir_path)
    
    try:
        with open(project['path'], 'w') as f:
            f.write(content)
        st.success(f"✅ Generated for {project['name']}: {project['path']}")
    except Exception as e:
        st.error(f"❌ Error generating for {project['name']}: {str(e)}")
