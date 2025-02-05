"""LLMテスターのメインアプリケーション"""

import gradio as gr
import openai
import json
from typing import Tuple

from app.utils import validate_inputs, get_ip_info
from app.ui import create_ui

def process_prompt(prompt: str, base_url: str, api_key: str, model: str, 
                  max_tokens: int, temperature: float, progress: gr.Progress = None) -> Tuple[str, str]:
    """プロンプトを処理してLLMの応答を取得する"""
    # 入力値の検証
    is_valid, error_message = validate_inputs(prompt, base_url, api_key)
    if not is_valid:
        return f"⚠️ 入力エラー: {error_message}", ""

    try:
        if progress:
            progress(0.3, desc="OpenAI クライアントを初期化中...")
            
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        if progress:
            progress(0.5, desc="LLMにリクエスト送信中...")
            
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if progress:
            progress(0.8, desc="レスポンスを処理中...")
            
        result = {
            "応答": response.choices[0].message.content,
            "デバッグ情報": {
                "ネットワーク情報": get_ip_info(),
                "APIレスポンス": json.dumps(response.model_dump(), indent=2, ensure_ascii=False)
            }
        }
        
        if progress:
            progress(1.0, desc="完了")
            
        return (
            f"✨ **応答**:\n\n{result['応答']}",
            f"🔍 **デバッグ情報**:\n```json\n{json.dumps(result['デバッグ情報'], indent=2, ensure_ascii=False)}\n```"
        )
        
    except Exception as e:
        error_detail = str(e)
        return (
            f"❌ **エラーが発生しました**\n\n{error_detail}",
            f"🔍 **エラー詳細**:\n```\n{error_detail}\n```"
        )

if __name__ == "__main__":
    interface = create_ui(process_prompt)
    interface.launch(
        server_name="0.0.0.0",
        server_port=80,
        share=False
    )
