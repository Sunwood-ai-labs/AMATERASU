"""
OpenWebUI APIのユーティリティ関数
"""

import json
from typing import Any, Dict, Optional
import requests
from requests.exceptions import RequestException
import config

def handle_api_error(response: requests.Response) -> None:
    """
    APIエラーを処理する

    Args:
        response (requests.Response): APIレスポンス

    Raises:
        Exception: APIエラーの詳細
    """
    try:
        error_data = response.json()
        error_message = error_data.get('error', {}).get('message', 'Unknown error')
    except json.JSONDecodeError:
        error_message = response.text or 'Unknown error'
    
    raise Exception(f"API Error ({response.status_code}): {error_message}")

def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    APIリクエストを実行する

    Args:
        method (str): HTTPメソッド
        endpoint (str): エンドポイントパス
        data (Optional[Dict[str, Any]], optional): リクエストボディ
        files (Optional[Dict[str, Any]], optional): アップロードするファイル
        params (Optional[Dict[str, Any]], optional): クエリパラメータ

    Returns:
        Dict[str, Any]: APIレスポンス

    Raises:
        Exception: APIリクエストエラー
    """
    url = f"{config.BASE_URL}{endpoint}"
    headers = config.get_headers()

    # デバッグ情報を表示
    print(f"リクエストURL: {url}")
    
    try:
        if files:
            # ファイルアップロード時はContent-Typeヘッダーを削除
            headers.pop("Content-Type", None)
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data if data and not files else None,
            files=files,
            params=params
        )
        
        if response.status_code >= 400:
            handle_api_error(response)
        
        # レスポンスの内容をデバッグ表示
        try:
            response_data = response.json()
            print(f"レスポンスステータス: {response.status_code}")
            return response_data
        except json.JSONDecodeError:
            print(f"JSONではないレスポンス: {response.text}")
        return response.json()
    
    except RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

def format_chat_messages(messages: list) -> list:
    """
    チャットメッセージを適切な形式にフォーマットする

    Args:
        messages (list): メッセージのリスト

    Returns:
        list: フォーマットされたメッセージのリスト
    """
    formatted_messages = []
    for msg in messages:
        if isinstance(msg, str):
            formatted_messages.append({
                "role": "user",
                "content": msg
            })
        elif isinstance(msg, dict):
            formatted_messages.append(msg)
    return formatted_messages
