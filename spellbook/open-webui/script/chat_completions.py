#!/usr/bin/env python3
"""
OpenWebUIのチャット完了APIを利用するCLIツール
"""

import argparse
import json
from typing import Dict, List, Any, Optional, Union
from . import config
from .utils import make_request, format_chat_messages

def create_chat_completion(
    model: str,
    messages: Union[List[Dict[str, str]], List[str]],
    files: Optional[List[Dict[str, str]]] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    チャット完了リクエストを実行する

    Args:
        model (str): 使用するモデルのID
        messages (Union[List[Dict[str, str]], List[str]]): チャットメッセージのリスト
        files (Optional[List[Dict[str, str]]], optional): 使用するファイルやコレクションのリスト
        **kwargs (Any): その他のオプションパラメータ

    Returns:
        Dict[str, Any]: チャット完了レスポンス
    """
    formatted_messages = format_chat_messages(messages)
    
    data = {
        "model": model,
        "messages": formatted_messages,
        **kwargs
    }
    
    if files:
        data["files"] = files
    
    return make_request(
        method="POST",
        endpoint=config.ENDPOINTS["chat_completions"],
        data=data
    )

def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(description="OpenWebUIのチャット完了APIを利用する")
    parser.add_argument(
        "message",
        help="送信するメッセージ"
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gpt-4-turbo",
        help="使用するモデルのID（デフォルト: gpt-4-turbo）"
    )
    parser.add_argument(
        "-f",
        "--file",
        help="使用するファイルのID"
    )
    parser.add_argument(
        "-c",
        "--collection",
        help="使用するコレクションのID"
    )
    parser.add_argument(
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
        files = None
        if args.file:
            files = [{"type": "file", "id": args.file}]
        elif args.collection:
            files = [{"type": "collection", "id": args.collection}]

        response = create_chat_completion(
            model=args.model,
            messages=[args.message],
            files=files
        )
        
        if args.json:
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "応答なし")
            print("\n=== モデルの応答 ===")
            print(content)
            print("==================")
            
    except Exception as e:
        print(f"エラー: {str(e)}")

if __name__ == "__main__":
    main()
