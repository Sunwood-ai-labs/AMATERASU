"""
Terraform変数ファイルジェネレーター
main-infrastructureディレクトリを持つプロジェクトに対して
terraform.tfvarsファイルを自動生成します
"""
from utils.ui_components import (
    initialize_page,
    discover_projects_with_ui,
    show_input_form,
    generate_files_with_progress
)
from utils.project_discovery import find_terraform_main_infrastructure_dirs

def main():
    """メイン関数"""
    # ページの初期化
    initialize_page()
    
    # プロジェクトの探索と表示
    projects = discover_projects_with_ui(find_terraform_main_infrastructure_dirs)
    
    # 入力フォームの表示とファイル生成
    show_input_form(projects, generate_files_with_progress)

if __name__ == "__main__":
    main()
