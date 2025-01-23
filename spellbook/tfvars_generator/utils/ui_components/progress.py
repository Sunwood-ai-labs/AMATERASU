"""
進捗表示のUIコンポーネントを提供するモジュール
"""
import streamlit as st
import time
import os
from config.terraform_values import (
    generate_main_tfvars_content,
    generate_cloudfront_tfvars_content
)
from config.project_values import ProjectValues
from utils.file_operations import write_tfvars

def generate_files_with_progress(projects, domain_name, project_settings):
    """
    terraform.tfvarsファイルを生成し、進捗状況を表示

    Args:
        projects (list): プロジェクト情報のリスト
        domain_name (str): ドメイン名
        project_settings (dict): プロジェクトごとの設定値
            {
                'project_name': {
                    'subdomain': str,
                    'project_name': str,
                    'instance_type': str,
                    'ami_id': str,
                    'key_name': str
                }
            }
    """
    st.divider()
    st.subheader("🔄 生成状況")
    
    # プログレスバーで進捗表示
    progress_text = "ファイル生成の進捗状況"
    progress_bar = st.progress(0, text=progress_text)
    
    total_steps = len(projects) * 2  # main-infrastructureとcloudfront-infrastructureの2ファイル
    current_step = 0
    
    for i, project in enumerate(projects):
        project_values = project_settings[project['name']]
        
        # 1. main-infrastructure/terraform.tfvarsの生成
        current_step += 1
        progress = current_step / total_steps
        progress_bar.progress(progress, text=f"main-infrastructure: {project['name']}")
        
        with st.spinner(f"💾 {project['name']}のmain-infrastructure設定を生成中..."):
            main_content = generate_main_tfvars_content(project_values)
            # pathキーとmain_tfvars_pathキーの両方に対応
            tfvars_path = project.get('main_tfvars_path') or project.get('path')
            if not tfvars_path:
                st.error(f"❌ {project['name']}: tfvarsファイルのパスが指定されていません")
                continue
                
            write_tfvars({
                'name': project['name'],
                'path': tfvars_path
            }, main_content)
            time.sleep(0.3)  # UIの動きを視覚化するための遅延
        
        # 2. cloudfront-infrastructure/terraform.tfvarsの生成
        current_step += 1
        progress = current_step / total_steps
        progress_bar.progress(progress, text=f"cloudfront-infrastructure: {project['name']}")
        
        with st.spinner(f"💾 {project['name']}のCloudFront設定を生成中..."):
            # CloudFrontの設定は、main_tfvars_pathとcloudfront_tfvars_pathの両方が必要
            main_tfvars = project.get('main_tfvars_path') or project.get('path')
            cloudfront_tfvars = project.get('cloudfront_tfvars_path')

            if not main_tfvars:
                st.error(f"❌ {project['name']}: main-infrastructureのパスが指定されていません")
                continue

            if cloudfront_tfvars:
                cloudfront_content = generate_cloudfront_tfvars_content(
                    project_values,
                    main_tfvars
                )
                write_tfvars({
                    'name': project['name'],
                    'path': cloudfront_tfvars
                }, cloudfront_content)
            time.sleep(0.3)  # UIの動きを視覚化するための遅延
    
    st.success("✨ 全てのファイルの生成が完了しました！")
    st.balloons()
