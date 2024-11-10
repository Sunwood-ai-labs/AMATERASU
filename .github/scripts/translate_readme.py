import os
import sys

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService

def display_content_preview(content, title):
    preview_length = 200  # プレビューの長さ（文字数）
    logger.info(f"{title}:\n{content[:preview_length]}...")

def main():
    logger.info("README翻訳プロセスを開始します。")

    logger.info("設定を読み込んでいます...")
    settings = get_settings()
    logger.success("設定の読み込みが完了しました。")

    logger.info("LLMサービスを初期化しています...")
    llm_service = LLMService()
    logger.success("LLMサービスの初期化が完了しました。")

    logger.info("README.mdファイルを読み込んでいます...")
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        logger.success("README.mdファイルの読み込みが完了しました。")
        display_content_preview(readme_content, "元のREADMEの冒頭")
    except FileNotFoundError:
        logger.error("README.mdファイルが見つかりません。")
        return
    except Exception as e:
        logger.error(f"README.mdファイルの読み込み中にエラーが発生しました: {str(e)}")
        return

    prompt = f"""
Please translate the following Japanese README into English:

```
{readme_content}
```
    """

    logger.info("LLMにREADMEの英訳を依頼しています...")
    try:
        translated_readme = llm_service.get_response(prompt, remove_code_block=True)
        logger.success("LLMからの英訳の取得が完了しました。")
        display_content_preview(translated_readme, "翻訳後のREADMEの冒頭")
    except Exception as e:
        logger.error(f"LLMからの英訳の取得中にエラーが発生しました: {str(e)}")
        return

    logger.info("翻訳されたREADMEを保存しています...")
    try:
        os.makedirs("docs", exist_ok=True)
        with open("docs/README.en.md", "w", encoding="utf-8") as f:
            f.write(translated_readme)
        logger.success("翻訳されたREADMEの保存が完了しました。")
    except Exception as e:
        logger.error(f"翻訳されたREADMEの保存中にエラーが発生しました: {str(e)}")
        return

    logger.info("READMEの英訳プロセスが正常に完了しました。")

if __name__ == "__main__":
    main()
