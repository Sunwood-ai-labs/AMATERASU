"""
プロジェクト一覧表示のUIコンポーネントを提供するモジュール
"""
import gradio as gr
from typing import List, Dict, Any, Callable

def show_project_list(
    projects: List[Any],  # TerraformProjectのリスト
    on_select: Callable[[List[str]], None]
) -> gr.Blocks:
    """
    プロジェクト一覧を表示するコンポーネント

    Args:
        projects (List[Any]): TerraformProjectオブジェクトのリスト
        on_select (Callable[[List[str]], None]): プロジェクト選択時のコールバック

    Returns:
        gr.Blocks: Gradioコンポーネント
    """
    with gr.Blocks() as project_list:
        gr.Markdown("## 📂 検出されたプロジェクト")
        
        if not projects:
            gr.Warning("⚠️ 対象となるプロジェクトが見つかりませんでした")
            return project_list
        
        gr.Markdown(f"合計 {len(projects)} 個のプロジェクトを検出しました")
        
        # プロジェクト選択チェックボックス
        project_checkboxes = []
        for project in projects:
            with gr.Row():
                checkbox = gr.Checkbox(
                    label=project["name"],
                    value=False,
                    info=f"インフラ定義: {project.get('infrastructure_dir', 'N/A')}"
                )
                project_checkboxes.append(checkbox)
                
                with gr.Column():
                    if hasattr(project, 'main_tfvars_path') and project.main_tfvars_path:
                        gr.Markdown("##### 🔧 Main Infrastructure")
                        gr.Code(project.main_tfvars_path, language="bash")
                    
                    if hasattr(project, 'cloudfront_tfvars_path') and project.cloudfront_tfvars_path:
                        gr.Markdown("##### 🌐 CloudFront Infrastructure")
                        gr.Code(project.cloudfront_tfvars_path, language="bash")
        
        # 全選択/解除ボタン
        with gr.Row():
            select_all = gr.Button("🔘 全て選択", variant="secondary")
            clear_all = gr.Button("⭕ 全て解除", variant="secondary")
        
        def update_all_checkboxes(value: bool) -> List[bool]:
            return [value] * len(project_checkboxes)
        
        select_all.click(
            fn=lambda: update_all_checkboxes(True),
            outputs=project_checkboxes
        )
        
        clear_all.click(
            fn=lambda: update_all_checkboxes(False),
            outputs=project_checkboxes
        )
        
        # プロジェクト選択の変更を監視
        def on_selection_change(*values):
            selected_projects = [
                project.name
                for project, selected in zip(projects, values)
                if selected
            ]
            on_select(selected_projects)
        
        for checkbox in project_checkboxes:
            checkbox.change(
                fn=on_selection_change,
                inputs=project_checkboxes,
                outputs=None
            )
    
    return project_list
