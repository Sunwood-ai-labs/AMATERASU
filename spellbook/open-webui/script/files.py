#!/usr/bin/env python3
"""
OpenWebUIのファイル操作とナレッジコレクション関連APIを利用するCLIツール
"""

import argparse
import json
import os
from typing import Dict, Any, Optional
from . import config
from .utils import make_request

def upload_file(file_path: str) -> Dict[str, Any]:
    """
    ファイルをアップロードする

    Args:
        file_path (str): アップロードするファイルのパス

    Returns:
        Dict[str, Any]: アップロード結果
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    with open(file_path, 'rb') as f:
        files = {'file': f}
        return make_request(
            method="POST",
            endpoint=config.ENDPOINTS["files"],
            files=files
        )

def add_file_to_knowledge(
    knowledge_id: str,
    file_id: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    ナレッジコレクションにファイルを追加する

    Args:
        knowledge_id (str): ナレッジコレクションのID
        file_id (str): 追加するファイルのID
        description (Optional[str], optional): ファイルの説明

    Returns:
        Dict[str, Any]: 追加結果
    """
    data = {
        "file_id": file_id
    }
    
    if description:
        data["description"] = description
    
    endpoint = config.ENDPOINTS["knowledge_file_add"].format(id=knowledge_id)
    return make_request(
        method="POST",
        endpoint=endpoint,
        data=data
    )

def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        description="OpenWebUIのファイル操作とナレッジコレクション関連APIを利用する"
    )
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # uploadコマンドの設定
    upload_parser = subparsers.add_parser("upload", help="ファイルをアップロードする")
    upload_parser.add_argument(
        "file_path",
        help="アップロードするファイルのパス"
    )
    upload_parser.add_argument(
        "--json",
        action="store_true",
        help="結果をJSON形式で出力"
    )

    # addコマンドの設定
    add_parser = subparsers.add_parser(
        "add",
        help="ファイルをナレッジコレクションに追加する"
    )
    add_parser.add_argument(
        "knowledge_id",
        help="ナレッジコレクションのID"
    )
    add_parser.add_argument(
        "file_id",
        help="追加するファイルのID"
    )
    add_parser.add_argument(
        "-d",
        "--description",
        help="ファイルの説明"
    )
    add_parser.add_argument(
        "--json",
        action="store_true",
        help="結果をJSON形式で出力"
    )

    return parser

def main():
    """メイン実行関数"""
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.command == "upload":
            result = upload_file(args.file_path)
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("\n=== アップロード結果 ===")
                print(f"ファイルID: {result.get('id', 'Unknown')}")
                print("=====================")

        elif args.command == "add":
            result = add_file_to_knowledge(
                args.knowledge_id,
                args.file_id,
                args.description
            )
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("\n=== 追加結果 ===")
                print("ファイルの追加が完了しました")
                print("===============")

        else:
            parser.print_help()
            
    except Exception as e:
        print(f"エラー: {str(e)}")

if __name__ == "__main__":
    main()
