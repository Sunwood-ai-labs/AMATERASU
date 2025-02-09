"""ユーティリティ関数"""

import socket
import requests
from typing import Dict, Tuple

def get_ip_info() -> Dict[str, str]:
    """IPとホスト名の情報を取得する"""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
    except Exception as e:
        public_ip = f"取得失敗 ({str(e)})"
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception as e:
        hostname = f"取得失敗 ({str(e)})"
        local_ip = "取得失敗"
        
    return {
        "パブリックIP": public_ip,
        "ローカルIP": local_ip,
        "ホスト名": hostname
    }

def validate_inputs(prompt: str, base_url: str, api_key: str) -> Tuple[bool, str]:
    """入力値の検証を行う"""
    if not prompt.strip():
        return False, "プロンプトを入力してください"
    if not base_url.strip():
        return False, "Proxy URLを入力してください"
    if not api_key.strip() or api_key == "your_api_key":
        return False, "有効なAPI Keyを入力してください"
    return True, ""
