"""
OpenWebUIのAPI設定モジュール
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# 実行フォルダの.envを読み込む
current_dir = Path(os.getcwd())
env_path = current_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)

load_dotenv()
# APIのベースURL
BASE_URL = os.getenv("OPENWEBUI_API_URL", "http://localhost:8282")
print(BASE_URL)

# APIキー
API_KEY: Optional[str] = os.getenv("OPENWEBUI_API_KEY")
if API_KEY:
    # APIキーが存在する場合のみ、最初の5文字を表示
    print(f"APIキー: {API_KEY[:5]}...")

# デフォルトのリクエストヘッダー
def get_headers(content_type: str = "application/json") -> dict:
    """
    APIリクエスト用のヘッダーを生成する

    Args:
        content_type (str): Content-Typeヘッダーの値

    Returns:
        dict: リクエストヘッダー
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": content_type
    }
    
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    return headers

# APIエンドポイント
ENDPOINTS = {
    "models": "/api/models",  # v1を追加
    "chat_completions": "/api/chat/completions",
    "files": "/api/v1/files/",
    "knowledge_file_add": "/api/v1/knowledge/{id}/file/add"
}
