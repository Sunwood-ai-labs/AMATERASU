#!/usr/bin/env python3
"""
OpenWebUIのモデル一覧を取得するCLIツール
"""

import argparse
import json
from typing import Dict, List, Any
import config
from utils import make_request
from loguru import logger

def list_models() -> Dict[str, Any]:
    """
    利用可能なモデルの一覧を取得する

    Returns:
        Dict[str, Any]: モデルの一覧を含むレスポンス

    Raises:
        Exception: APIリクエストエラー
    """
    logger.debug("モデル一覧の取得を開始")
    response = make_request(
        method="GET",
        endpoint="/api/models"  # 正しいエンドポイントを使用
    )
    logger.debug("モデル一覧の取得が完了")
    return response

def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(description="OpenWebUIの利用可能なモデル一覧を取得")
    parser.add_argument(
        "--json",
        action="store_true",
        help="結果をJSON形式で出力"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="デバッグモードで実行"
    )
    return parser

def main():
    """メイン実行関数"""
    parser = create_parser()
    args = parser.parse_args()

    # デバッグモードが指定された場合はログレベルを変更
    if args.debug:
        logger.remove()
        logger.add(
            sink=lambda msg: print(msg, end=""),
            format="<level>{level: <8}</level> | <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
            colorize=True,
            level="DEBUG"
        )
        logger.debug("デバッグモードで実行中")

    try:
        logger.info("OpenWebUIのモデル一覧を取得しています...")
        response = list_models()
        
        # レスポンスの型をチェック
        if isinstance(response, str):
            logger.error(f"APIレスポンス: {response}")
            return
            
        if args.json:
            print(json.dumps(response, indent=2, ensure_ascii=False))
            logger.info("JSON形式でモデル一覧を出力しました")
        else:
            logger.success("モデル一覧を取得しました")
            
            # データフィールドからモデル一覧を取得
            if isinstance(response, dict) and 'data' in response:
                models = response['data']
                
                if isinstance(models, list):
                    logger.info(f"取得したモデル数: {len(models)}")
                    
                    for model in models:
                        model_id = model.get('id', 'Unknown ID')
                        model_name = model.get('name', 'Unknown Name')
                        model_owned_by = model.get('owned_by', 'Unknown Owner')
                        
                        logger.info(f"モデル: {model_name} ({model_id})")
                        logger.info(f"  所有者: {model_owned_by}")
                        
                        # その他の情報があれば表示
                        if 'object' in model:
                            logger.info(f"  タイプ: {model['object']}")
                        
                        # OpenAI情報がある場合は表示
                        if 'openai' in model and isinstance(model['openai'], dict):
                            logger.info("  OpenAI情報:")
                            for key, value in model['openai'].items():
                                logger.info(f"    {key}: {value}")
                        
                        # パイプ情報がある場合は表示
                        if 'pipe' in model and isinstance(model['pipe'], dict):
                            logger.info(f"  パイプタイプ: {model['pipe'].get('type', 'Unknown')}")
                        
                        logger.info("") # 空行を入れる
                else:
                    logger.warning("モデル情報が見つかりませんでした")
            else:
                # レスポンス形式が異なる場合はそのまま表示
                logger.warning("予期しないレスポンス形式:")
                for key, value in response.items():
                    logger.info(f"{key}: {value}")
                
    except Exception as e:
        logger.exception(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
