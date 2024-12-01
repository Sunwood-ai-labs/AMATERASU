import os
import gitlab
import sys
import json

class GitLabSetup:
    def __init__(self, url, token, project_id):
        """GitLabセットアップの初期化"""
        self.gl = gitlab.Gitlab(url, private_token=token)
        self.project_id = project_id
        self.project = self.gl.projects.get(project_id)
        
    def create_pipeline_trigger(self, description="Auto Issue Labeler Trigger"):
        """パイプライントリガーの作成"""
        try:
            # 既存のトリガーをチェック
            triggers = self.project.triggers.list()
            for trigger in triggers:
                if trigger.description == description:
                    print(f"Trigger already exists with token: {trigger.token}")
                    return trigger.token
            
            # 新しいトリガーを作成
            trigger = self.project.triggers.create({'description': description})
            print(f"Created new trigger with token: {trigger.token}")
            return trigger.token
            
        except Exception as e:
            print(f"Error creating trigger: {str(e)}")
            return None

    def setup_webhook(self, trigger_token):
        """Webhookの設定"""
        try:
            webhook_url = f"{self.gl.url}/api/v4/projects/{self.project_id}/ref/main/trigger/pipeline?token={trigger_token}&variables[TRIGGER_SOURCE]=issue"
            
            # 既存のWebhookをチェック
            hooks = self.project.hooks.list()
            for hook in hooks:
                if hook.url == webhook_url:
                    print("Webhook already exists!")
                    return True
            
            # 新しいWebhookを作成
            hook = self.project.hooks.create({
                'url': webhook_url,
                'issues_events': True,
                'push_events': False,
                'enable_ssl_verification': False
            })
            print(f"Created webhook with ID: {hook.id}")
            return True
            
        except Exception as e:
            print(f"Error setting up webhook: {str(e)}")
            return False

    def setup_ci_variables(self, variables):
        """CI/CD変数の設定"""
        try:
            existing_vars = self.project.variables.list()
            existing_var_keys = [v.key for v in existing_vars]
            
            for key, value in variables.items():
                if key in existing_var_keys:
                    print(f"Variable {key} already exists")
                    continue
                
                self.project.variables.create({
                    'key': key,
                    'value': value,
                    'protected': False,
                    'masked': True
                })
                print(f"Created variable: {key}")
                
        except Exception as e:
            print(f"Error setting up CI variables: {str(e)}")

def main():
    # GitLabの設定
    GITLAB_URL = "http://amaterasu-gitlab-dev.sunwood-ai-labs.click"
    GITLAB_TOKEN = os.getenv("GITLAB_API_TOKEN")
    PROJECT_ID = 1
    
    if not GITLAB_TOKEN:
        print("Error: GITLAB_API_TOKEN environment variable not set")
        sys.exit(1)
    
    # GitLabセットアップの実行
    setup = GitLabSetup(GITLAB_URL, GITLAB_TOKEN, PROJECT_ID)
    
    # トリガーの作成
    trigger_token = setup.create_pipeline_trigger()
    if not trigger_token:
        sys.exit(1)
    
    # Webhookの設定
    if not setup.setup_webhook(trigger_token):
        sys.exit(1)
    
    # 必要なCI/CD変数の設定
    variables = {
        'TRIGGER_TOKEN': trigger_token,
        # 他の必要な変数があればここに追加
    }
    setup.setup_ci_variables(variables)
    
    # 設定情報の出力
    config = {
        'trigger_token': trigger_token,
        'webhook_url': f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/ref/main/trigger/pipeline"
    }
    print("\nConfiguration complete!")
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()
