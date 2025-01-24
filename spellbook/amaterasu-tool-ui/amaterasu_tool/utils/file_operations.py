"""
ファイル操作機能を提供するモジュール
"""
import os
import shutil
from dataclasses import dataclass
from typing import List, Set, Optional

@dataclass
class DeletedItem:
    """削除されたアイテムの情報"""
    name: str
    path: str
    type: str  # "file" or "directory"

@dataclass
class SkippedItem:
    """スキップされたアイテムの情報"""
    name: str
    path: str
    reason: str

class FileOperationResult:
    """ファイル操作の結果を格納するクラス"""
    def __init__(self):
        self.deleted_items: List[DeletedItem] = []
        self.skipped_items: List[SkippedItem] = []
        self.errors: List[str] = []

    @property
    def success(self) -> bool:
        """操作が成功したかどうか"""
        return len(self.errors) == 0

    def add_deleted(self, name: str, path: str, type_: str) -> None:
        """削除されたアイテムを追加"""
        self.deleted_items.append(DeletedItem(name, path, type_))

    def add_skipped(self, name: str, path: str, reason: str) -> None:
        """スキップされたアイテムを追加"""
        self.skipped_items.append(SkippedItem(name, path, reason))

    def add_error(self, error: str) -> None:
        """エラーを追加"""
        self.errors.append(error)

class FileOperations:
    """ファイル操作を提供するクラス"""

    @staticmethod
    def ensure_directory(path: str) -> None:
        """
        ディレクトリが存在することを確認し、存在しない場合は作成

        Args:
            path (str): 作成するディレクトリのパス
        """
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """
        ファイルに内容を書き込む

        Args:
            path (str): 書き込み先のファイルパス
            content (str): 書き込む内容
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
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

    @staticmethod
    def delete_terraform_cache(project_path: str) -> FileOperationResult:
        """
        Terraformのキャッシュファイルを削除

        Args:
            project_path (str): terraform.tfvarsファイルのパス

        Returns:
            FileOperationResult: 削除操作の結果
        """
        result = FileOperationResult()
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
                        result.add_deleted(name, abs_path, "directory")
                    else:
                        os.remove(abs_path)
                        result.add_deleted(name, abs_path, "file")
                except Exception as e:
                    result.add_error(f"{abs_path}の削除に失敗しました: {str(e)}")
            else:
                result.add_skipped(name, abs_path, "存在しないためスキップ")

        return result
