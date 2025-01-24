"""
ファイル操作に関するユーティリティ関数を提供するモジュール
"""
import os
import shutil
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class FileOperationResult:
    """ファイル操作の結果を格納するクラス"""
    success: bool
    message: str
    deleted_items: List[Dict[str, str]]
    skipped_items: List[Dict[str, str]]

def write_file(path: str, content: str) -> FileOperationResult:
    """
    ファイルに内容を書き込む

    Args:
        path (str): 書き込み先のファイルパス
        content (str): 書き込む内容

    Returns:
        FileOperationResult: 操作の結果
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return FileOperationResult(
            success=True,
            message=f"ファイルを正常に保存しました: {path}",
            deleted_items=[],
            skipped_items=[]
        )
    except Exception as e:
        return FileOperationResult(
            success=False,
            message=f"ファイルの保存に失敗しました: {str(e)}",
            deleted_items=[],
            skipped_items=[]
        )

def read_file(path: str) -> Optional[str]:
    """
    ファイルの内容を読み込む

    Args:
        path (str): 読み込むファイルのパス

    Returns:
        Optional[str]: ファイルの内容。ファイルが存在しない場合はNone
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def delete_terraform_cache(project_path: str) -> FileOperationResult:
    """
    Terraformのキャッシュファイルを削除

    Args:
        project_path (str): terraform.tfvarsファイルのパス

    Returns:
        FileOperationResult: 削除操作の結果
    """
    deleted_items = []
    skipped_items = []
    
    try:
        abs_dir_path = os.path.abspath(os.path.dirname(project_path))
        
        # 削除対象のファイル・ディレクトリ
        cache_paths = {
            '.terraform': os.path.join(abs_dir_path, '.terraform'),
            'terraform.tfstate': os.path.join(abs_dir_path, 'terraform.tfstate'),
            'terraform.tfstate.backup': os.path.join(abs_dir_path, 'terraform.tfstate.backup'),
            '.terraform.lock.hcl': os.path.join(abs_dir_path, '.terraform.lock.hcl')
        }
        
        for name, path in cache_paths.items():
            abs_path = os.path.abspath(path)
            
            if os.path.exists(abs_path):
                try:
                    if os.path.isdir(abs_path):
                        shutil.rmtree(abs_path)
                        deleted_items.append({
                            'name': name,
                            'path': abs_path,
                            'type': 'directory'
                        })
                    else:
                        os.remove(abs_path)
                        deleted_items.append({
                            'name': name,
                            'path': abs_path,
                            'type': 'file'
                        })
                except Exception as e:
                    return FileOperationResult(
                        success=False,
                        message=f"{abs_path}の削除に失敗しました: {str(e)}",
                        deleted_items=deleted_items,
                        skipped_items=skipped_items
                    )
            else:
                skipped_items.append({
                    'name': name,
                    'path': abs_path,
                    'reason': '存在しないためスキップ'
                })
        
        return FileOperationResult(
            success=True,
            message="キャッシュの削除が完了しました",
            deleted_items=deleted_items,
            skipped_items=skipped_items
        )
        
    except Exception as e:
        return FileOperationResult(
            success=False,
            message=f"キャッシュ削除でエラーが発生しました: {str(e)}",
            deleted_items=deleted_items,
            skipped_items=skipped_items
        )
