"""
プロジェクト探索に関するユーティリティ関数を提供するモジュール
"""
import os
import glob
from typing import List, Dict, Any

def find_terraform_infrastructure_dirs(base_path: str = "..") -> List[Dict[str, Any]]:
    """
    terraform/main-infrastructureとterraform/cloudfront-infrastructureの
    両方のディレクトリを持つプロジェクトを探索

    Args:
        base_path (str): 探索を開始するベースディレクトリのパス
               デフォルトは".."（親ディレクトリ）

    Returns:
        List[Dict[str, Any]]: 検出されたプロジェクトの情報を含む辞書のリスト
              各辞書は以下の形式:
              {
                  'name': 'プロジェクト名',
                  'main_tfvars_path': 'main-infrastructure/terraform.tfvarsへのパス',
                  'cloudfront_tfvars_path': 'cloudfront-infrastructure/terraform.tfvarsへのパス',
                  'output_json_path': 'main-infrastructure/output.jsonへのパス'
              }
    """
    projects = []
    abs_base_path = os.path.abspath(base_path)

    for project_dir in glob.glob(os.path.join(abs_base_path, "*/")):
        abs_project_dir = os.path.abspath(project_dir)
        terraform_dir = os.path.join(abs_project_dir, "terraform")
        main_infra_dir = os.path.join(terraform_dir, "main-infrastructure")
        cloudfront_infra_dir = os.path.join(terraform_dir, "cloudfront-infrastructure")

        # 両方のディレクトリが存在する場合のみ処理
        if os.path.exists(main_infra_dir) and os.path.exists(cloudfront_infra_dir):
            project_name = os.path.basename(abs_project_dir)

            if project_name and project_name != "terraform":
                projects.append({
                    'name': project_name,
                    'main_tfvars_path': os.path.join(main_infra_dir, "terraform.tfvars"),
                    'cloudfront_tfvars_path': os.path.join(cloudfront_infra_dir, "terraform.tfvars"),
                    'output_json_path': os.path.join(main_infra_dir, "output.json"),
                    'abs_path': abs_project_dir,
                    'infrastructure_dir': main_infra_dir
                })

    projects.sort(key=lambda x: x['name'])
    return projects

def find_terraform_main_infrastructure_dirs(base_path: str = "..") -> List[Dict[str, Any]]:
    """
    terraform/main-infrastructureディレクトリを持つプロジェクトを探索

    Args:
        base_path (str): 探索を開始するベースディレクトリのパス
               デフォルトは".."（親ディレクトリ）

    Returns:
        List[Dict[str, Any]]: 検出されたプロジェクトの情報を含む辞書のリスト
               各辞書は以下の形式:
               {
                   'name': 'プロジェクト名',
                   'path': 'terraform.tfvarsファイルへのパス',
                   'abs_path': 'tfvarsファイルの絶対パス',
                   'infrastructure_dir': 'mainインフラディレクトリのパス'
               }
    """
    projects = []
    
    # ベースパスを絶対パスに変換
    abs_base_path = os.path.abspath(base_path)
    
    # terraform/main-infrastructureディレクトリを持つプロジェクトを探索
    for project_dir in glob.glob(os.path.join(abs_base_path, "*/")):
        # プロジェクトディレクトリを絶対パスに変換
        abs_project_dir = os.path.abspath(project_dir)
        terraform_dir = os.path.join(abs_project_dir, "terraform/main-infrastructure")
        
        if os.path.exists(terraform_dir):
            # terraform/main-infrastructureの2階層上のディレクトリ名をプロジェクト名として取得
            infrastructure_parent = os.path.dirname(terraform_dir)  # terraform/
            project_dir = os.path.dirname(infrastructure_parent)   # プロジェクトディレクトリ
            project_name = os.path.basename(project_dir)          # プロジェクト名
            
            tfvars_path = os.path.join(terraform_dir, "terraform.tfvars")
            
            # プロジェクト名が実際のプロジェクトディレクトリから取得できた場合のみ追加
            if project_name and project_name != "terraform":
                projects.append({
                    'name': project_name,
                    'path': tfvars_path,
                    'abs_path': os.path.abspath(tfvars_path),  # 絶対パスも保持
                    'infrastructure_dir': terraform_dir  # mainインフラディレクトリのパスも保持
                })
    
    # プロジェクト名でソート
    projects.sort(key=lambda x: x['name'])
    
    return projects
