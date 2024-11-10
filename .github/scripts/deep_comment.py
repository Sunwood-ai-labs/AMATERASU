from loguru import logger
import sys
import os

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService

def main():
    logger.info("イシューの深堀処理を開始します。")
    
    settings = get_settings()
    llm_service = LLMService()
    github_service = GitHubService()

    logger.info("GitHubからイシューを取得中...")
    issue = github_service.get_issue()
    logger.info(f"イシュー「{issue.title}」を取得しました。")
    
    logger.info("リポジトリの概要を読み込み中...")
    with open(settings.REPOSITORY_SUMMARY_PATH, "r", encoding="utf-8") as f:
        repository_summary = f.read()
    logger.info("リポジトリの概要を読み込みました。")

    prompt = f"""
以下のGitHubイシューに対して、リポジトリの情報を踏まえた詳細なコメントを生成してください：

イシュータイトル: {issue.title}
イシュー本文: {issue.body}

リポジトリの概要:
{repository_summary}

詳細なコメント:
    """

    logger.info("LLMを使用して深いコメントを生成中...")
    deep_comment = llm_service.get_response(prompt)
    logger.info("深いコメントの生成が完了しました。")

    logger.info("生成したコメントをGitHubイシューに追加中...")
    github_service.add_comment(issue, deep_comment)
    logger.info("コメントをイシューに追加しました。")

    logger.info("イシューの深堀処理が正常に完了しました。")

if __name__ == "__main__":
    main()
