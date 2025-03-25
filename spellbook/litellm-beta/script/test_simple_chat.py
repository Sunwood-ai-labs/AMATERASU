import openai
from loguru import logger
import json
import time
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# APIの設定
API_BASE = os.getenv("API_BASE")
MODEL_NAME = os.getenv("MODEL_NAME")

# OpenAIクライアントの初期化
client = openai.OpenAI(
    api_key="sk-1234",  # litellm proxyでは実際のキーは不要
    base_url=API_BASE
)

def test_chat():
    """通常のチャット補完をテストする"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "あなたは親切で簡潔なアシスタントです。"},
                {"role": "user", "content": "プログラミングについて5行で説明してください。"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        logger.info("チャット補完が正常に生成されました")
        logger.info(f"使用モデル: {response.model}")
        logger.info(f"応答内容: {response.choices[0].message.content}")
        logger.info(f"使用トークン数: {response.usage.total_tokens}")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        logger.exception("エラーの詳細:")

def test_json_mode():
    """JSON形式での応答をテストする"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "JSONフォーマットで応答してください。"},
                {"role": "user", "content": """
                以下の情報を含むユーザープロファイルをJSONで生成してください：
                - 名前
                - 年齢
                - 職業
                - 趣味（配列）
                - 好きな食べ物（配列）
                """}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}  # JSON モードを指定
        )
        
        logger.info("JSON形式での応答が正常に生成されました")
        logger.info(f"使用モデル: {response.model}")
        logger.info("応答内容:")
        # JSONとしてパースして整形して表示
        parsed_content = json.loads(response.choices[0].message.content)
        logger.info(json.dumps(parsed_content, indent=2, ensure_ascii=False))
        
    except Exception as e:
        if "429" in str(e):
            logger.warning("レートリミットに達しました。しばらく待ってから再試行してください。")
        else:
            logger.error(f"エラーが発生しました: {str(e)}")
            logger.exception("エラーの詳細:")

if __name__ == "__main__":
    # ロギングの設定
    logger.add("simple_chat_test_{time}.log")
    
    logger.info(f"チャット補完テストを開始します\nAPI接続先: {API_BASE}")
    
    # 通常のチャット補完テスト
    logger.info("=== 通常のチャット補完テスト ===")
    test_chat()
    
    # レートリミット対策のために待機
    logger.info("次のリクエストまで60秒待機します...")
    time.sleep(60)
    
    # JSONモードのテスト
    logger.info("\n=== JSON形式でのテスト ===")
    # test_json_mode()
