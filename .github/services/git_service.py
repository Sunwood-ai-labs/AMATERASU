import subprocess
from typing import List
from loguru import logger
from config import get_settings

class GitService:
    def __init__(self):
        self.settings = get_settings()

    def setup_credentials(self):
        repo_url = f"https://x-access-token:{self.settings.GITHUB_TOKEN}@github.com/{self.settings.GITHUB_REPOSITORY}.git"
        subprocess.run(["git", "remote", "set-url", "origin", repo_url])
        logger.info("Git credentials setup completed.")

    def create_branch(self, branch_name: str):
        subprocess.run(["git", "checkout", "-b", branch_name])
        logger.info(f"ブランチ '{branch_name}' を作成しました。")

    def commit_changes(self, file_paths: List[str], commit_message: str):
        for file_path in file_paths:
            subprocess.run(["git", "add", file_path])
        
        cmd = ["git", "commit", "-m", commit_message]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Commit failed: {result.stderr}")
            raise RuntimeError("Git commit failed")
        logger.info(f"変更をコミットしました: {commit_message}")

    def push_changes(self, branch_name: str):
        result = subprocess.run(["git", "push", "-u", "origin", branch_name], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Push failed: {result.stderr}")
            raise RuntimeError("Git push failed")
        logger.info(f"変更を {branch_name} ブランチにプッシュしました。")
