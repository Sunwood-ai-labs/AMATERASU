"""
Terraformキャッシュを管理するページ
"""
import os
import streamlit as st
from utils.project_discovery import find_terraform_main_infrastructure_dirs
from utils.file_operations import delete_terraform_cache

def format_path_for_display(path):
    """
    パスを表示用にフォーマット
    ホームディレクトリを~に置換し、見やすく整形

    Args:
        path (str): 整形するパス
    Returns:
        str: 整形されたパス
    """
    home = os.path.expanduser("~")
    if path.startswith(home):
        path = "~" + path[len(home):]
    return path

def show_cache_manager():
    """キャッシュ管理UIを表示"""
    st.title("🗑️ Terraform Cache Manager")
    st.markdown("""
    ### 概要
    このページでは、選択したプロジェクトのTerraformキャッシュを削除できます。
    """)

    # 削除対象ファイルの説明
    with st.expander("ℹ️ 削除対象ファイル", expanded=False):
        st.markdown("""
        以下のファイルが削除対象となります：
        - `.terraform/`
        - `terraform.tfstate`
        - `terraform.tfstate.backup`
        - `.terraform.lock.hcl`
        """)

    # プロジェクトの取得
    projects = find_terraform_main_infrastructure_dirs()
    
    if not projects:
        st.warning("⚠️ 対象プロジェクトが見つかりませんでした")
        return

    # プロジェクト選択UI
    st.subheader("📂 プロジェクト選択")
    
    # 全選択/解除ボタン
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔘 全て選択", key="cache_select_all"):
            for project in projects:
                st.session_state[f"cache_select_{project['name']}"] = True
        if st.button("⭕ 全て解除", key="cache_clear_all"):
            for project in projects:
                st.session_state[f"cache_select_{project['name']}"] = False
    
    st.divider()
    
    # プロジェクト一覧
    selected_projects = []
    for project in projects:
        with st.container():
            if st.checkbox(
                f"📁 {project['name']}",
                key=f"cache_select_{project['name']}",  # キーにプレフィックスを追加
                help=f"インフラ定義: {format_path_for_display(project['infrastructure_dir'])}"
            ):
                selected_projects.append(project)
            
            # プロジェクトの詳細情報を小さく表示
            st.caption(f"📍 {format_path_for_display(project['abs_path'])}")
    
    # 選択プロジェクトの表示と処理
    if selected_projects:
        st.divider()
        st.markdown(f"#### 🎯 選択されたプロジェクト ({len(selected_projects)}個)")
        
        # 選択されたプロジェクトの一覧を表示
        with st.expander("📋 選択プロジェクト一覧", expanded=True):
            for project in selected_projects:
                st.code(
                    f"📁 {project['name']}\n└─ {format_path_for_display(project['abs_path'])}",
                    language="bash"
                )
        
        # 削除ボタン
        st.markdown("### ⚠️ 操作の実行")
        st.warning(f"{len(selected_projects)}個のプロジェクトのキャッシュを削除します。")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button(
                "✅ 削除実行",
                type="primary",
                key="cache_confirm_delete",  # キーにプレフィックスを追加
                use_container_width=True
            ):
                progress_text = "キャッシュ削除の進捗"
                progress_bar = st.progress(0, text=progress_text)
                
                for i, project in enumerate(selected_projects):
                    progress = (i + 1) / len(selected_projects)
                    progress_bar.progress(
                        progress,
                        text=f"処理中: {project['name']} ({i+1}/{len(selected_projects)})"
                    )
                    
                    with st.spinner(f"🔄 {project['name']}のキャッシュを削除中..."):
                        delete_terraform_cache(project['abs_path'])
                
                st.success("✨ キャッシュの削除が完了しました！")
                st.balloons()
        
        with col2:
            if st.button(
                "❌ キャンセル",
                key="cache_cancel_delete",  # キーにプレフィックスを追加
                use_container_width=True
            ):
                st.rerun()
    else:
        st.info("ℹ️ キャッシュを削除するプロジェクトを選択してください")

def main():
    """メイン関数"""
    show_cache_manager()

if __name__ == "__main__":
    main()
