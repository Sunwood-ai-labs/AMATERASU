import gitlab
import sys
from typing import List, Optional

def setup_webhook(
    gitlab_url: str,
    gitlab_token: str,
    webhook_url: str,
    project_id: Optional[int] = None,
    group_id: Optional[int] = None
) -> None:
    """
    GitLabプロジェクトまたはグループにWebhookを設定する
    
    Args:
        gitlab_url: GitLabのURL
        gitlab_token: GitLabのアクセストークン
        webhook_url: 設定するWebhookのURL
        project_id: 特定のプロジェクトID（省略可）
        group_id: 特定のグループID（省略可）
    """
    # GitLabクライアントの初期化
    gl = gitlab.Gitlab(
        gitlab_url,
        private_token=gitlab_token
    )

    webhook_config = {
        'url': webhook_url,
        'push_events': False,
        'issues_events': True,  # Issueイベントのみを有効化
        'confidential_issues_events': True,
        'note_events': False,
        'merge_requests_events': False,
        'tag_push_events': False,
        'pipeline_events': False,
        'wiki_page_events': False,
        'enable_ssl_verification': False,  # 開発環境用（本番環境ではTrueにすることを推奨）
    }

    try:
        if project_id:
            # 特定のプロジェクトにWebhookを設定
            project = gl.projects.get(project_id)
            hooks = project.hooks.list()
            
            # 既存のWebhookをチェック
            for hook in hooks:
                if hook.url == webhook_url:
                    print(f"Webhook already exists for project {project_id}")
                    return
            
            # 新しいWebhookを作成
            hook = project.hooks.create(webhook_config)
            print(f"Successfully created webhook for project {project_id}")

        elif group_id:
            # グループ全体にWebhookを設定
            group = gl.groups.get(group_id)
            hooks = group.hooks.list()
            
            # 既存のWebhookをチェック
            for hook in hooks:
                if hook.url == webhook_url:
                    print(f"Webhook already exists for group {group_id}")
                    return
            
            # 新しいWebhookを作成
            hook = group.hooks.create(webhook_config)
            print(f"Successfully created webhook for group {group_id}")

        else:
            raise ValueError("Either project_id or group_id must be provided")

    except gitlab.exceptions.GitlabAuthenticationError:
        print("Authentication failed. Please check your GitLab token.")
        sys.exit(1)
    except gitlab.exceptions.GitlabGetError:
        print(f"Failed to get project/group. Please check if the ID exists and you have proper permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # GitLab設定
    GITLAB_URL = "http://192.168.0.131"
    GITLAB_TOKEN = "glpat-KpMd3Kb8QT_g29ydeWrL"
    
    # Webhookの設定
    WEBHOOK_URL = "http://192.168.0.131:8000/webhook"  # サーバーのIPアドレスに変更してください
    
    # プロジェクトIDまたはグループIDを指定（どちらか一方）
    PROJECT_ID = None  # 例: 123
    GROUP_ID = None    # 例: 456
    
    if PROJECT_ID is None and GROUP_ID is None:
        print("Please specify either PROJECT_ID or GROUP_ID in the script.")
        sys.exit(1)
    
    setup_webhook(
        gitlab_url=GITLAB_URL,
        gitlab_token=GITLAB_TOKEN,
        webhook_url=WEBHOOK_URL,
        project_id=PROJECT_ID,
        group_id=GROUP_ID
    )
