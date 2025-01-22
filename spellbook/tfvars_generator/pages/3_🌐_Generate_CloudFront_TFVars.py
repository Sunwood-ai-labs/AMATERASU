"""
cloudfront-infrastructure用のterraform.tfvarsファイルを生成するページ
"""
import os
import streamlit as st
import time
from utils.ui_components import (
    discover_projects_with_ui,
    show_input_form
)
from utils.project_discovery import find_terraform_infrastructure_dirs
from config.terraform_values import (
    get_terraform_values,
    generate_cloudfront_tfvars_content
)
from utils.file_operations import write_tfvars

def select_projects(projects):
    """
    プロジェクトの選択UIを表示

    Args:
        projects (list): 検出されたプロジェクトのリスト

    Returns:
        list: 選択されたプロジェクトのリスト
    """
    st.divider()
    st.subheader("📂 プロジェクト選択")

    # 全選択/解除ボタン
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔘 全て選択"):
            for project in projects:
                st.session_state[f"select_{project['name']}"] = True
        if st.button("⭕ 全て解除"):
            for project in projects:
                st.session_state[f"select_{project['name']}"] = False

    st.divider()

    # プロジェクトの選択UI
    selected_projects = []
    for project in projects:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.checkbox(
                "📁",
                key=f"select_{project['name']}",
                help=f"選択: {project['name']}"
            ):
                selected_projects.append(project)
        
        with col2:
            with st.expander(project['name'], expanded=True):
                st.markdown("##### 🔧 Main Infrastructure")
                st.code(project['main_tfvars_path'])
                st.markdown("##### 🌐 CloudFront Infrastructure")
                st.code(project['cloudfront_tfvars_path'])

    return selected_projects

def show_current_values():
    """現在の設定値を表示"""
    values = get_terraform_values()
    
    with st.expander("🛠️ 現在のインフラ設定", expanded=True):
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
        
        with col2:
            st.markdown("#### 🔍 Route53設定")
            if values.get('ROUTE53'):
                st.code(f"""
Zone ID: {values['ROUTE53'].get('zone_id', 'N/A')}
Zone Name: {values['ROUTE53'].get('zone_name', 'N/A')}
Internal Zone ID: {values['ROUTE53'].get('internal_zone_id', 'N/A')}
Internal Zone Name: {values['ROUTE53'].get('internal_zone_name', 'N/A')}
""")

def generate_cloudfront_files_with_progress(projects, domain_name, project_settings):
    """
    CloudFront用のterraform.tfvarsファイルを生成し、進捗状況を表示
    """
    st.divider()
    st.subheader("🔄 生成状況")
    
    # プログレスバーで進捗表示
    progress_text = "ファイル生成の進捗状況"
    progress_bar = st.progress(0, text=progress_text)
    
    total_steps = len(projects)
    current_step = 0
    
    for i, project in enumerate(projects):
        current_step += 1
        progress = current_step / total_steps
        progress_bar.progress(progress, text=f"CloudFront設定: {project['name']}")
        
        with st.spinner(f"💾 {project['name']}のCloudFront設定を生成中..."):
            # output.jsonの存在確認
            output_exists = os.path.exists(project['output_json_path'])
            if not output_exists:
                st.warning(f"⚠️ {project['name']}: output.jsonが見つかりません。デフォルト値を使用します。")
            
            try:
                project_values = project_settings[project['name']]
                cloudfront_content = generate_cloudfront_tfvars_content(
                    project_values,
                    project['main_tfvars_path']
                )
                write_tfvars({
                    'name': project['name'],
                    'path': project['cloudfront_tfvars_path']
                }, cloudfront_content)
                
                st.success(f"✅ {project['name']}: CloudFront設定の生成が完了しました")
                
            except Exception as e:
                st.error(f"❌ {project['name']}: エラーが発生しました - {str(e)}")
                continue
            
            time.sleep(0.3)  # UIの動きを視覚化するための遅延
    
    if current_step > 0:
        st.success("✨ 全てのファイルの生成が完了しました！")
        st.balloons()

def main():
    """メイン関数"""
    st.title("🌐 CloudFront Variables Generator")
    st.markdown("""
    ### 概要
    このページでは、選択したプロジェクトに対してCloudFrontの設定ファイルを生成します：

    1. 🔍 **プロジェクト選択**
       - main-infrastructureとcloudfront-infrastructureを持つプロジェクトから選択
       - 必要なプロジェクトのみを選んで処理

    2. 🌐 **CloudFront設定**
       - オリジンドメインの設定
       - カスタムドメインの設定
       - セキュリティ設定

    3. 🔗 **オリジンサーバー連携**
       - main-infrastructureのEC2との連携
       - Route53ドメイン設定

    ⚠️ **注意**:
    1. まず`Generate TFVars`ページでmain-infrastructure用の設定を生成してください。
    2. main-infrastructure/output.jsonが存在しないプロジェクトはデフォルト値を使用します。
    """)
    
    # 現在の設定値を表示
    show_current_values()
    
    # プロジェクトの探索（CloudFrontとmain-infrastructureの両方を持つプロジェクトのみ）
    projects = discover_projects_with_ui(find_terraform_infrastructure_dirs)
    
    if not projects:
        st.warning("⚠️ main-infrastructureとcloudfront-infrastructureの両方を持つプロジェクトが見つかりませんでした")
        return
    
    # プロジェクトの選択
    selected_projects = select_projects(projects)
    
    if not selected_projects:
        st.warning("⚠️ 処理するプロジェクトを選択してください")
        return
    
    # 選択されたプロジェクトの数を表示
    st.success(f"✅ {len(selected_projects)}個のプロジェクトが選択されました")
    
    # 入力フォームの表示と選択したプロジェクトの処理
    show_input_form(selected_projects, generate_cloudfront_files_with_progress)

if __name__ == "__main__":
    main()
