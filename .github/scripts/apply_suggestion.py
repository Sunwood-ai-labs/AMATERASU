import sys
import os

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService
from services.git_service import GitService
from utils.diff_utils import DiffUtils, create_comment
from utils.patch_utils import apply_patch, get_patch_file_path

class SuggestionApplier:
    def __init__(self):
        self.settings = get_settings()
        self.llm_service = LLMService()
        self.github_service = GitHubService()
        self.git_service = GitService()
        # self.allowed_users = self.settings.ALLOWED_USERS  # 設定から許可されたユーザーのリストを取得

    def run(self):
        logger.info("変更提案の適用処理を開始します。")
        
        issue = self.github_service.get_issue()
        all_comments = self.github_service.get_comments(issue)
        
        # コメントユーザーの一覧を表示
        self._display_comment_users(all_comments)
        
        # 許可されたユーザーのコメントのみをフィルタリング
        # comments = self._filter_allowed_comments(all_comments)
        comments = all_comments

        if not self._validate_comments(comments):
            return

        previous_comment = self._find_previous_bot_comment(comments)
        if not previous_comment:
            logger.error("Error: github-actions[bot] のコメントが見つかりませんでした。")
            raise ValueError("github-actions[bot] のコメントが見つかりません")

        print(previous_comment.body)
        diffs = DiffUtils.extract_diff(previous_comment.body)
        if diffs is None:
            logger.error("有効なdiffを抽出できませんでした。処理を終了します。")
            return

        try:
            modified_files = self._process_diffs(diffs)
            self._create_pull_request(issue, modified_files)
        except Exception as e:
            logger.error(f"エラーが発生しました: {str(e)}")
            raise

    # def _filter_allowed_comments(self, comments):
    #     """許可されたユーザーのコメントのみをフィルタリングする"""
    #     return [comment for comment in comments if comment.user.login in self.allowed_users]

    def _display_comment_users(self, comments):
        """コメントをしているユーザーの一覧を表示する"""
        user_list = list(set(comment.user.login for comment in comments))
        logger.info(f"コメントをしているユーザーの一覧:")
        for user in user_list:
            logger.info(f"- {user}")

    def _validate_comments(self, comments):
        comment_count = len(comments)
        logger.info(f"イシュー #{self.settings.ISSUE_NUMBER} のコメントを {comment_count}件取得しました。")

        if comment_count == 0 or comments[-1].body.strip().lower() != "ok":
            logger.warning("最後のコメントが 'ok' ではありません。処理を終了します。")
            # return False
            return True
        
        logger.info("'ok' コメントを確認しました。")
        return True

    def _find_previous_bot_comment(self, comments, bot_name="github-actions[bot]"):
        logger.info("直前の github-actions[bot] のコメントを探しています。")
        return next((comment for comment in reversed(comments[:-1]) if comment.user.login == "Sunwood-ai-labs"), None)

    def _process_diffs(self, diffs):
        modified_files = []
        for file_path, diff_content in diffs.items():
            logger.info(f"{file_path} のパッチ適用を試みます。")
            patch_file_path = get_patch_file_path(file_path)
            with open(patch_file_path, 'w', encoding='utf-8') as f:
                f.write(diff_content)
            print(diff_content)
            if apply_patch(patch_file_path, file_path):
                modified_files.append(file_path)
            else:
                logger.info(f"{file_path} のパッチ適用に失敗しました。LLMを使用して変更を生成します。")
                self._apply_llm_changes(file_path, diff_content)
                modified_files.append(file_path)
        return modified_files

    def _apply_llm_changes(self, file_path, diff_content):
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
        modified_content = self.llm_service.apply_diff(original_content, diff_content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

    def _create_pull_request(self, issue, modified_files):
        branch_name = f"suggestion-issue-{self.settings.ISSUE_NUMBER}"
        self.git_service.setup_credentials()
        self.git_service.create_branch(branch_name)
        self.git_service.commit_changes(modified_files, f"🤖 #{self.settings.ISSUE_NUMBER} の提案を適用")
        self.git_service.push_changes(branch_name)

        comment = create_comment(modified_files, {file: open(file, "r").read() for file in modified_files})
        self.github_service.add_comment(issue, comment)
        logger.info(f"イシュー #{issue.number} にコメントを追加しました。")

        pr_title = f"イシュー #{self.settings.ISSUE_NUMBER} の提案"
        pr_body = f"このPRはイシュー #{self.settings.ISSUE_NUMBER} の提案を適用しています。"
        self.github_service.create_pull_request(pr_title, pr_body, branch_name)

def main():
    applier = SuggestionApplier()
    applier.run()

if __name__ == "__main__":
    main()
