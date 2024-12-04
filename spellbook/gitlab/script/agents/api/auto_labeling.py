from fastapi import FastAPI, Request
from typing import List, Dict
import gitlab
import openai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 定数の定義
API_BASE = "https://amaterasu-litellm-dev.sunwood-ai-labs.click"
GITLAB_URL = "http://192.168.0.131"
GITLAB_TOKEN = "glpat-KpMd3Kb8QT_g29ydeWrL"

# FastAPIアプリケーションの初期化
app = FastAPI()

# GitLabクライアントの設定
gl = gitlab.Gitlab(
    GITLAB_URL,
    private_token=GITLAB_TOKEN
)

# OpenAIクライアントの初期化
client = openai.OpenAI(
    api_key="sk-1234",  # litellm proxyでは実際のキーは不要
    base_url=API_BASE
)

# 利用可能なラベルのリスト
AVAILABLE_LABELS = [
    'bug', 'feature', 'documentation', 'enhancement', 'question',
    'security', 'performance', 'ui/ux', 'testing', 'maintenance'
]

class GitLabWebhookEvent(BaseModel):
    object_kind: str
    project: Dict
    object_attributes: Dict

def get_labels_from_llm(title: str, description: str) -> List[str]:
    """
    litellm proxy経由でLLMを使用してテキストを分析し、適切なラベルを取得する
    """
    try:
        response = client.chat.completions.create(
            model="bedrock/claude-3-5-sonnet",
            messages=[
                {"role": "system", "content": f"""
                あなたはGitLabのissueに適切なラベルを付けるアシスタントです。
                以下のラベルから、issueの内容に最も適したものを1つ以上選んでください:
                {', '.join(AVAILABLE_LABELS)}
                
                応答は以下のJSON形式で返してください:
                {{"labels": ["label1", "label2"]}}
                """},
                {"role": "user", "content": f"""
                Title: {title}
                Description: {description}
                """}
            ],
            temperature=0.3,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        
        result = response.choices[0].message.content
        labels = eval(result)['labels']
        return [label for label in labels if label in AVAILABLE_LABELS]
        
    except Exception as e:
        print(f"Error in label generation: {str(e)}")
        return []

@app.post("/webhook")
async def handle_webhook(request: Request):
    event = await request.json()
    
    # issueイベント以外は無視
    if event.get('object_kind') != 'issue':
        return {"status": "skipped", "message": "Not an issue event"}
        
    try:
        # issueの内容を取得
        project_id = event['project']['id']
        issue_iid = event['object_attributes']['iid']
        title = event['object_attributes']['title']
        description = event['object_attributes']['description'] or ''
        
        # プロジェクトとissueの取得
        project = gl.projects.get(project_id)
        issue = project.issues.get(issue_iid)
        
        # LLMを使用してラベルを取得
        labels_to_add = get_labels_from_llm(title, description)
        
        # 既存のラベルを保持しつつ、新しいラベルを追加
        current_labels = issue.labels
        new_labels = list(set(current_labels + labels_to_add))
        
        # ラベルの更新
        if labels_to_add:
            issue.labels = new_labels
            issue.save()
            
        return {
            "status": "success",
            "added_labels": labels_to_add,
            "current_labels": new_labels
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
