"""
プロジェクト一覧表示のUIコンポーネントを提供するモジュール
"""
import streamlit as st
import time

def show_project_list(projects):
    """
    検出されたプロジェクトの一覧を表示

    Args:
        projects (list): プロジェクト情報のリスト
    """
    st.divider()
    st.subheader("📂 検出されたプロジェクト")
    
    if projects:
        # プログレスバーでプロジェクト数を表示
        progress_text = f"合計 {len(projects)} 個のプロジェクトを検出"
        project_progress = st.progress(0, text=progress_text)
        project_progress.progress(1.0)
        
        # プロジェクト一覧をカラムで表示
        for i, project in enumerate(projects):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**{project['name']}**")
            with col2:
                st.code(project['path'], language="bash")
            
            # 最後以外は区切り線を表示
            if i < len(projects) - 1:
                st.divider()
    else:
        st.warning("⚠️ terraform/main-infrastructureディレクトリを持つプロジェクトが見つかりませんでした")

def discover_projects_with_ui(find_projects_func):
    """
    プロジェクトを探索してUI表示

    Args:
        find_projects_func (callable): プロジェクト探索関数

    Returns:
        list: 検出されたプロジェクトのリスト
    """
    with st.spinner("🔍 プロジェクトを探索中..."):
        time.sleep(1)  # UIの動きを視覚化するための遅延
        projects = find_projects_func()
    
    show_project_list(projects)
    return projects
