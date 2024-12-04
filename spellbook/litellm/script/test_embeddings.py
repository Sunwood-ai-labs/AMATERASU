import os
from litellm import embedding
import json
from typing import List, Dict
import time
from loguru import logger
import sys

# 定数定義
API_BASE = "https://amaterasu-litellm-dev.sunwood-ai-labs.click"  # 末尾のスラッシュを削除

# ログの設定
logger.remove()  # デフォルトのハンドラーを削除
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "embedding_test_{time}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 day"
)

def test_embedding(
    model_name: str,
    test_texts: List[str],
    print_dimensions: bool = True
) -> Dict:
    """
    指定されたモデルで埋め込みテストを実行する関数
    
    Args:
        model_name: テストする埋め込みモデルの名前
        test_texts: テストに使用するテキストのリスト
        print_dimensions: 埋め込みの次元数を表示するかどうか
        
    Returns:
        テスト結果を含む辞書
    """
    logger.info(f"Starting embedding test for model: {model_name}")
    logger.debug(f"Test texts: {test_texts}")

    try:
        start_time = time.time()
        
        # 埋め込みの実行
        logger.debug(f"Executing embedding for {model_name}")
        response = embedding(
            model=model_name,
            input=test_texts,
            api_base=API_BASE
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 結果の解析
        embeddings = response['data']
        dimension = len(embeddings[0]['embedding'])
        
        result = {
            "model": model_name,
            "status": "success",
            "dimension": dimension,
            "processing_time": processing_time,
            "token_usage": response.get('usage', {})
        }
        
        logger.success(f"Successfully generated embeddings for {model_name}")
        logger.info(f"Dimension: {dimension}")
        logger.info(f"Processing time: {processing_time:.2f} seconds")
        logger.info(f"Token usage: {json.dumps(response.get('usage', {}), indent=2)}")
        
        # 実際の埋め込みベクトルの一部をサンプル表示
        logger.debug(f"Sample embedding vector (first 5 dimensions): {embeddings[0]['embedding'][:5]}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error testing {model_name}: {str(e)}")
        logger.exception("Full exception details:")
        return {
            "model": model_name,
            "status": "error",
            "error": str(e)
        }

def main():
    logger.info("Starting embedding model tests")
    
    # テストするテキスト
    test_texts = [
        "This is a test sentence in English",
        # "これは日本語のテストセンテンスです",
        # "This is another test sentence to ensure consistency"
    ]
    
    # テストする埋め込みモデル (configに合わせたモデル名を使用)
    embedding_models = [
        "bedrock/amazon.titan-embed-text-v1",    # config.yamlのmodel_nameと一致させる
        # "bedrock/cohere.embed-english-v3",       # config.yamlのmodel_nameと一致させる
        # "bedrock/cohere.embed-multilingual-v3"   # config.yamlのmodel_nameと一致させる
    ]
    
    logger.info(f"Using API base: {API_BASE}")
    
    # 各モデルのテスト実行
    results = []
    for model in embedding_models:
        logger.info(f"Testing model: {model}")
        result = test_embedding(model, test_texts)
        results.append(result)
    
    # 結果のサマリー出力
    logger.info("=== Test Summary ===")
    for result in results:
        status = "✅" if result["status"] == "success" else "❌"
        if result["status"] == "success":
            logger.success(f"{status} {result['model']}")
            logger.info(f"  Dimension: {result['dimension']}")
            logger.info(f"  Processing time: {result['processing_time']:.2f}s")
        else:
            logger.error(f"{status} {result['model']}")
            logger.error(f"  Error: {result['error']}")

if __name__ == "__main__":
    main()
