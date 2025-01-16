"""
プロジェクト探索に関するユーティリティ関数を提供するモジュール
"""
import os
import glob

def find_terraform_main_infrastructure_dirs(base_path=".."):
    """
    terraform/main-infrastructureディレクトリを持つプロジェクトを探索

    Args:
        base_path (str): 探索を開始するベースディレクトリのパス
               デフォルトは".."（親ディレクトリ）

    Returns:
        list: 検出されたプロジェクトの情報を含む辞書のリスト
              各辞書は以下の形式:
              {
                  'name': 'プロジェクト名',
                  'path': 'terraform.tfvarsファイルへのパス'
              }
    """
    projects = []
    
    # terraform/main-infrastructureディレクトリを持つプロジェクトを探索
    for project_dir in glob.glob(f"{base_path}/*/"):
        terraform_dir = os.path.join(project_dir, "terraform/main-infrastructure")
        if os.path.exists(terraform_dir):
            project_name = os.path.basename(os.path.dirname(project_dir))
            projects.append({
                'name': project_name,
                'path': os.path.join(terraform_dir, "terraform.tfvars")
            })
    
    # プロジェクト名でソート
    projects.sort(key=lambda x: x['name'])
    
    return projects
