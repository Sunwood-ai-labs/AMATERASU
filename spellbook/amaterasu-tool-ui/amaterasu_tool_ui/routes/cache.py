"""
キャッシュ管理ページのロジックを提供するモジュール
"""
import gradio as gr
from amaterasu_tool import AmaterasuTool
from typing import List, Dict, Any
from amaterasu_tool_ui.components import (
    show_project_list,
    show_cache_cleaning_progress
)

def create_cache_page() -> gr.Blocks:
    """
    キャッシュ管理ページを作成

    Returns:
        gr.Blocks: Gradioページコンポーネント
    """
    with gr.Blocks() as page:
        gr.Markdown("# 🧹 Terraform Cache Manager")
        gr.Markdown("""
        ### 📝 概要
        このページでは、選択したプロジェクトのTerraformキャッシュを削除できます。

        以下のファイルが削除対象となります：
        - `.terraform/`
        - `terraform.tfstate`
        - `terraform.tfstate.backup`
        - `.terraform.lock.hcl`
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
        
        with gr.Row():
            # 削除確認ダイアログ
            with gr.Group():
                gr.Markdown("### ⚠️ 操作の実行")
                
                with gr.Row():
                    delete_button = gr.Button(
                        "✅ 削除実行",
                        variant="primary",
                        scale=1
                    )
                    cancel_button = gr.Button(
                        "❌ キャンセル",
                        variant="secondary",
                        scale=1
                    )
        
        # 進捗表示領域
        progress_area = gr.Column(visible=False)
        
        def on_delete(project_names: List[str]) -> None:
            """キャッシュ削除処理"""
            if not project_names:
                gr.Warning("⚠️ プロジェクトが選択されていません")
                return
            
            progress_area.visible = True
            target_projects = [p for p in projects if p["name"] in project_names]
            
            for project in target_projects:
                tool.clean_terraform_cache(project["path"])
            
            show_cache_cleaning_progress(target_projects)
        
        # キャンセルボタンの処理
        def on_cancel() -> None:
            progress_area.visible = False
            selected_projects.value = []
        
        # ボタンのイベントハンドラを設定
        delete_button.click(
            fn=on_delete,
            inputs=[selected_projects],
            outputs=[progress_area]
        )
        
        cancel_button.click(
            fn=on_cancel,
            outputs=[progress_area]
        )
    
    return page
