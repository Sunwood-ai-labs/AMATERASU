"""
設定フォームのUIコンポーネントを提供するモジュール
"""
import gradio as gr
from typing import Dict, Any, List, Optional
from config.project_values import ProjectValues

def show_settings_form(
    project: Dict[str, Any],
    platform_name: Optional[str] = None,
    platform_short_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    プロジェクトごとの設定フォームを表示

    Args:
        project (Dict[str, Any]): プロジェクト情報
        platform_name (Optional[str]): プラットフォームの正式名称
        platform_short_name (Optional[str]): プラットフォームの略式名称

    Returns:
        gr.Blocks: Gradioコンポーネント
    """
    # 利用可能なパスを順番に試す
    tfvars_path = (
        project.get('path') or  # 後方互換性のため
        project.get('main_tfvars_path') or  # メインインフラ用
        project.get('cloudfront_tfvars_path')  # CloudFront用
    )
    values = ProjectValues(tfvars_path)
    folder_name = project['name'].lower()

    with gr.Blocks() as settings_form:
        gr.Markdown(f"## 🛠️ {project['name']} の設定")
        
        with gr.Row():
            with gr.Column():
                # サブドメインの設定
                default_subdomain = (
                    f"{platform_name}-{folder_name}"
                    if platform_name else values.get_value('subdomain', '')
                )
                subdomain = gr.Textbox(
                    label="サブドメイン",
                    value=default_subdomain,
                    info="例: amaterasu-coder"
                )
                
                # プロジェクト名の設定
                default_project_name = (
                    f"{platform_short_name}-{folder_name}"
                    if platform_short_name else values.get_value('project_name', '')
                )
                project_name = gr.Textbox(
                    label="プロジェクト名",
                    value=default_project_name,
                    info="例: amts-coder"
                )
                
                # インスタンスタイプの設定
                instance_type = gr.Dropdown(
                    label="インスタンスタイプ",
                    choices=['t3.micro', 't3.small', 't3.medium', 't3.large'],
                    value=values.get_value('instance_type', 't3.micro'),
                    info="EC2インスタンスのタイプを選択"
                )
            
            with gr.Column():
                # AMI IDの設定
                ami_id = gr.Textbox(
                    label="AMI ID",
                    value=values.get_value('ami_id', 'ami-0bba69335379e17f8'),
                    info="例: ami-0bba69335379e17f8"
                )
                
                # キーペア名の設定
                key_name = gr.Textbox(
                    label="キーペア名",
                    value=values.get_value('key_name', ''),
                    info="例: myapp-key"
                )
        
        # 設定プレビュー
        with gr.Accordion("⚡ 設定内容をプレビュー", open=False):
            preview = gr.Code(
                label="terraform.tfvars",
                language="hcl",
                interactive=False
            )
            
            def update_preview(subdomain_val, project_name_val, instance_type_val, ami_id_val, key_name_val):
                return f'''# Project Settings
project_name = "{project_name_val}"
subdomain    = "{subdomain_val}"

# Instance Settings
instance_type = "{instance_type_val}"
ami_id       = "{ami_id_val}"
key_name     = "{key_name_val}"'''
            
            # プレビューの自動更新
            for input_component in [subdomain, project_name, instance_type, ami_id, key_name]:
                input_component.change(
                    fn=update_preview,
                    inputs=[subdomain, project_name, instance_type, ami_id, key_name],
                    outputs=[preview]
                )

    return settings_form

def show_global_settings() -> gr.Blocks:
    """
    グローバル設定フォームを表示

    Returns:
        gr.Blocks: Gradioコンポーネント
    """
    with gr.Blocks() as global_settings:
        gr.Markdown("## ⚙️ 共通設定")
        
        with gr.Row():
            platform_name = gr.Textbox(
                label="プラットフォーム正式名称",
                value="amaterasu",
                info="例: amaterasu",
                placeholder="正式名称を入力してください"
            )
            
            platform_short_name = gr.Textbox(
                label="プラットフォーム略式名称",
                value="amts",
                info="例: amts",
                placeholder="略式名称を入力してください"
            )
        
        domain_name = gr.Textbox(
            label="共通ドメイン名",
            value="sunwood-ai-labs",
            info="例: sunwood-ai-labs",
            placeholder="ドメイン名を入力してください"
        )
    
    return global_settings
