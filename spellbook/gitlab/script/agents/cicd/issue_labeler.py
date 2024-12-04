import os
import gitlab
from litellm import completion
import json

class GitLabIssueLabeler:
    def __init__(self, gitlab_url, private_token, gemini_api_key):
        """
        GitLabIssueLabeler の初期化
        
        Args:
            gitlab_url (str): GitLabのURL
            private_token (str): GitLab Private Token
            gemini_api_key (str): Gemini API Key
        """
        self.gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        
        # 利用可能なラベルの定義
        self.available_labels = {
            "バグ": "予期しない動作や問題",
            "機能改善": "新機能のリクエストや改善提案",
            "ドキュメント": "ドキュメントの改善や追加",
            "質問": "追加情報や確認が必要",
            "ヘルプ募集": "サポートが必要",
            "初心者向け": "新規貢献者向けの課題",
            "パフォーマンス": "性能に関する問題",
            "セキュリティ": "セキュリティに関する懸念"
        }

    def analyze_issue_content(self, title, description):
        """
        Gemini を使用して issue の内容を分析し、適切なラベルを提案
        
        Args:
            title (str): Issue のタイトル
            description (str): Issue の説明
            
        Returns:
            list: 提案されたラベルのリスト
        """
        prompt = f"""
        以下のGitLab issueを分析し、適切なラベルを提案してください。
        選択可能なラベル:
        {json.dumps(self.available_labels, indent=2, ensure_ascii=False)}

        Issue タイトル: {title}
        Issue 説明: {description}

        最も関連性の高いラベルを最大3つまで選び、JSON配列形式で返してください。
        日本語のラベル名のみを返してください。
        """

        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            suggested_labels = json.loads(response.choices[0].message.content)
            return [label for label in suggested_labels if label in self.available_labels]
        except (json.JSONDecodeError, AttributeError, IndexError):
            return []

    def process_issue(self, project_id, issue_iid):
        """
        指定された issue に対してラベル付けを実行
        
        Args:
            project_id (int): プロジェクトID
            issue_iid (int): Issue IID
        """
        project = self.gl.projects.get(project_id)
        issue = project.issues.get(issue_iid)
        
        if not issue.labels:  # ラベルが付いていない場合のみ処理
            suggested_labels = self.analyze_issue_content(issue.title, issue.description)
            if suggested_labels:
                issue.labels = suggested_labels
                issue.save()
                print(f"Issue #{issue_iid} に以下のラベルを追加しました: {', '.join(suggested_labels)}")

def main():
    # 環境変数から設定を読み込み
    gitlab_url = os.getenv("CI_SERVER_URL", "http://gitlab")
    gitlab_token = os.getenv("GITLAB_API_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    project_id = os.getenv("CI_PROJECT_ID")
    issue_iid = os.getenv("CI_ISSUE_IID")
    
    if not all([gitlab_token, gemini_api_key, project_id, issue_iid]):
        raise ValueError("必要な環境変数が設定されていません")
    
    # ラベラーの初期化と実行
    labeler = GitLabIssueLabeler(gitlab_url, gitlab_token, gemini_api_key)
    labeler.process_issue(int(project_id), int(issue_iid))

if __name__ == "__main__":
    main()
