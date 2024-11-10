import sys
import os

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService
import os

def save_prompt(prompt, issue_number):
    prompt_dir = "generated_prompts"
    os.makedirs(prompt_dir, exist_ok=True)
    file_path = os.path.join(prompt_dir, f"prompt_issue_{issue_number}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    logger.info(f"プロンプトを {file_path} に保存しました。")

def main():
    logger.info("変更提案の生成を開始します。")
    
    settings = get_settings()
    llm_service = LLMService()
    github_service = GitHubService()

    issue = github_service.get_issue()
    logger.info(f"イシュー '{issue.title}' を取得しました。")
    
    # リポジトリの概要を取得する
    with open(settings.REPOSITORY_SUMMARY_PATH, "r", encoding="utf-8") as f:
        repository_summary = f.read()
    logger.info("リポジトリの概要を読み込みました。")

    prompt = f"""
以下のGitHubイシューに対して、リポジトリの情報を踏まえた具体的なコード変更提案を生成してください：

イシュータイトル: {issue.title}
イシュー本文: {issue.body}

リポジトリの概要:
{repository_summary}

変更提案（diff形式で記述してください）:
```diff
# ここにdiff形式の変更提案を記述
```
    """

    # プロンプトを保存
    save_prompt(prompt, issue.number)

    logger.info("LLMにプロンプトを送信します。")
    suggestion = llm_service.get_response(prompt)
    logger.info("LLMから変更提案を受け取りました。")

    github_service.add_comment(issue, f"## 変更提案\n\n{suggestion}")
    logger.info("変更提案をイシューにコメントとして追加しました。")

    logger.info("処理が正常に完了しました。")

if __name__ == "__main__":
    main()
