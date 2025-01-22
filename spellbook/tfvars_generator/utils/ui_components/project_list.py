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
            with st.expander(f"📁 {project['name']}", expanded=True):
                # プロジェクトの詳細情報を表示
                if 'main_tfvars_path' in project:
                    st.markdown("##### 🔧 Main Infrastructure")
                    st.code(project['main_tfvars_path'], language="bash")
                
                if 'cloudfront_tfvars_path' in project:
                    st.markdown("##### 🌐 CloudFront Infrastructure")
                    st.code(project['cloudfront_tfvars_path'], language="bash")
                
                if 'path' in project:
                    # 後方互換性のため
                    st.markdown("##### 📄 設定ファイル")
                    st.code(project['path'], language="bash")
            
            # 最後以外は区切り線を表示
            if i < len(projects) - 1:
                st.divider()
    else:
        st.warning("⚠️ 対象となるプロジェクトが見つかりませんでした")

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
