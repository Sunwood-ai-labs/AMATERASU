import openai
from loguru import logger

# APIの設定
API_BASE = "https://amaterasu-litellm-dev.sunwood-ai-labs.click"

# OpenAIクライアントの初期化
client = openai.OpenAI(
    api_key="sk-1234",  # litellm proxyでは実際のキーは不要
    base_url=API_BASE
)

def test_embedding():
    try:
        # 埋め込みの実行
        response = client.embeddings.create(
            model="bedrock/amazon.titan-embed-text-v1",
            input=["This is a test sentence in English", "これは日本語のテストです"]
        )
        
        # レスポンスの表示
        logger.info("Embedding generated successfully!")
        logger.info(f"Model used: {response.model}")
        logger.info(f"Embedding dimension: {len(response.data[0].embedding)}")
        logger.info(f"Total tokens used: {response.usage.total_tokens}")
        
        # 最初のベクトルの一部を表示
        logger.debug(f"First few dimensions of the first embedding: {response.data[0].embedding[:5]}")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    # ロギングの設定
    logger.add("simple_embedding_test_{time}.log")
    
    logger.info(f"Starting embedding test using {API_BASE}")
    test_embedding()
