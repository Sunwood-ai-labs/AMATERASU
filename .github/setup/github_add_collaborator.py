import os
import sys
from dotenv import load_dotenv
from github import Github
import github
from pathlib import Path
from loguru import logger

def load_env_files():
    load_dotenv()
    
    work_env = Path.cwd() / '.env'
    if work_env.exists():
        load_dotenv(work_env)
    logger.info("環境ファイルを読み込みました")

def add_collaborator_to_repo(repo_full_name, collaborator):
    token = os.getenv('GITHUB_ACCESS_TOKEN')
    if not token:
        logger.error("GITHUB_ACCESS_TOKEN 環境変数が設定されていません。")
        sys.exit(1)

    g = Github(token)

    try:
        repo = g.get_repo(repo_full_name)
        repo.add_to_collaborators(collaborator)
        logger.success(f"{repo_full_name} に {collaborator} をコラボレーターとして追加しました。")

    except github.GithubException as e:
        logger.error(f"エラーが発生しました: {e.status} {e.data}")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        logger.error("使用方法: python script.py <リポジトリ名> <コラボレーター名>")
        sys.exit(1)

    repo_full_name = sys.argv[1]
    collaborator = sys.argv[2]
    
    load_env_files()
    logger.info(f"{repo_full_name} リポジトリに {collaborator} をコラボレーターとして追加を開始します")
    add_collaborator_to_repo(repo_full_name, collaborator)

# ---------------------------
# コマンドメモ
#
# python .github\setup\github_add_collaborator.py Sunwood-ai-labs/x-archive-visualizer iris-s-coon
