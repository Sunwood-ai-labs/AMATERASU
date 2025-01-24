"""
CloudFront用terraform.tfvarsファイル生成ページのロジックを提供するモジュール
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

def create_cloudfront_page() -> gr.Blocks:
    """
    CloudFront用terraform.tfvarsファイル生成ページを作成

    Returns:
        gr.Blocks: Gradioページコンポーネント
    """
    with gr.Blocks() as page:
        gr.Markdown("# 🌐 CloudFront Variables Generator")
        gr.Markdown("""
        ### 📝 概要
        このページでは、選択したプロジェクトに対してCloudFrontの設定ファイルを生成します。

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
        
        # プロジェクトの探索と一覧表示
        tool = AmaterasuTool()
        projects = tool.find_projects(require_cloudfront=True)
        
        # 選択されたプロジェクトを保持する状態
        selected_projects = gr.State([])
        
        # プロジェクト一覧の表示
        def on_project_select(project_names: List[str]) -> None:
            selected_projects.value = [
                p for p in projects 
                if p["name"] in project_names
            ]
        
        project_list = show_project_list(projects, on_project_select)
        
        with gr.Form(id="cloudfront_form"):
            # グローバル設定
            global_settings = show_global_settings()
            
            # 選択されたプロジェクトの設定フォーム
            project_settings = {}
            for project in projects:
                project_settings[project["name"]] = show_settings_form(
                    project,
                    platform_name=global_settings["platform_name"].value,
                    platform_short_name=global_settings["platform_short_name"].value
                )
            
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
            target_projects = [p for p in projects if p["name"] in project_names]
            
            for project in target_projects:
                terraform_config = tool.load_terraform_config(project["output_json_path"])
                project_config = tool.load_project_config(project["main_tfvars_path"])
                
                content = terraform_config.generate_cloudfront_tfvars(
                    project_config,
                    origin_domain=f"{project_config.subdomain}.{domain_name}"
                )
                
                tool.file_operations.write_file(
                    project["cloudfront_tfvars_path"],
                    content
                )
            
            show_file_generation_progress(target_projects)
        
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
