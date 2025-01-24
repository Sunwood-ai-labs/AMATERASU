"""
terraform.tfvarsファイル生成ページのロジックを提供するモジュール
"""
import gradio as gr
from amaterasu_tool import AmaterasuTool
from typing import List, Dict, Any
from amaterasu_tool_ui.components import (
    show_project_list,
    show_settings_form,
    show_global_settings,
    show_file_generation_progress
)

def create_generate_page() -> gr.Blocks:
    """
    terraform.tfvarsファイル生成ページを作成

    Returns:
        gr.Blocks: Gradioページコンポーネント
    """
    with gr.Blocks() as page:
        gr.Markdown("# 🎮 Terraform Variables Generator")
        gr.Markdown("""
        ### 📝 概要
        このツールは、プロジェクトのterraform.tfvarsファイルを生成します。
        以下の設定が含まれます：

        - 🖥️ EC2インスタンスの基本設定
        - 🔒 VPCやセキュリティグループの設定
        - 🌐 Route53の内部ドメイン設定
        - 🔑 SSHキーや環境変数の設定
        """)
        
        # プロジェクトの探索と一覧表示
        tool = AmaterasuTool()
        projects = tool.find_projects()

        # 選択されたプロジェクトを保持する状態
        selected_projects = gr.State([])
        
        # プロジェクト一覧の表示
        def on_project_select(project_names: List[str]) -> None:
            selected_projects.value = [
                p for p in projects 
                if p["name"] in project_names
            ]
        
        project_list = show_project_list(projects, on_project_select)
        
        with gr.Form(id="tfvars_form"):
            # グローバル設定
            global_settings = show_global_settings()
            
            # 選択されたプロジェクトの設定フォーム
            project_settings = {}
            for project in projects:
                project_settings[project["name"]] = show_settings_form(project)
            
            # 生成ボタン
            generate_button = gr.Button(
                "🚀 生成開始",
                variant="primary",
                scale=2
            )
        
        # 生成結果の表示領域
        result_area = gr.Column(visible=False)
        
        def on_generate(
            project_names: List[str],
            platform_name: str,
            platform_short: str,
            domain_name: str
        ) -> None:
            """ファイル生成処理"""
            if not project_names:
                gr.Warning("⚠️ プロジェクトが選択されていません")
                return
            
            if not domain_name:
                gr.Warning("⚠️ ドメイン名を入力してください")
                return
            
            result_area.visible = True
            show_file_generation_progress(
                [p for p in projects if p["name"] in project_names]
            )
        
        # フォーム送信時の処理
        generate_button.click(
            fn=on_generate,
            inputs=[
                selected_projects,
                global_settings["platform_name"],
                global_settings["platform_short_name"],
                global_settings["domain_name"]
            ],
            outputs=[result_area]
        )
    
    return page
