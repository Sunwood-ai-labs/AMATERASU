from fastapi import FastAPI, Request, HTTPException
from typing import List, Dict, Optional
import gitlab
import openai
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pyngrok import ngrok
import uvicorn
import json
from loguru import logger
from functools import lru_cache

from fastapi.responses import RedirectResponse

# 環境変数の読み込み
load_dotenv()

# 環境変数から設定を読み込む
API_BASE = os.getenv("API_BASE", "https://amaterasu-litellm-dev.sunwood-ai-labs.click")
GITLAB_URL = os.getenv("GITLAB_URL", "http://192.168.0.131")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "glpat-KpMd3Kb8QT_g29ydeWrL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "sk-1234")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")
ENV = os.getenv("ENV", "development")

# FastAPIアプリケーションの初期化
app = FastAPI(title="GitLab Webhook Service",
             description="自動ラベル付けのためのGitLab Webhookサービス",
             version="1.0.0")

# GitLabクライアントの設定
@lru_cache()
def get_gitlab_client():
    return gitlab.Gitlab(
        GITLAB_URL,
        private_token=GITLAB_TOKEN
    )

# OpenAIクライアントの初期化
@lru_cache()
def get_openai_client():
    return openai.OpenAI(
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

def parse_llm_response(response_text: str) -> List[str]:
    """
    LLMの応答テキストからラベルのリストを抽出する
    """
    # コンマ区切りのテキストをリストに分割し、前後の空白を削除
    labels = [label.strip() for label in response_text.split(',')]
    # 利用可能なラベルのみをフィルタリング
    return [label for label in labels if label in AVAILABLE_LABELS]

def get_labels_from_llm(title: str, description: str) -> List[str]:
    """
    litellm proxy経由でLLMを使用してテキストを分析し、適切なラベルを取得する
    """
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="bedrock/claude-3-5-sonnet",
            messages=[
                {"role": "system", "content": f"""
                あなたはGitLabのissueに適切なラベルを付けるアシスタントです。
                以下のラベルから、issueの内容に最も適したものを1つ以上選んでください:
                {', '.join(AVAILABLE_LABELS)}
                
                応答は単純にカンマ区切りのテキストで返してください。
                例: bug, enhancement
                """},
                {"role": "user", "content": f"""
                Title: {title}
                Description: {description}
                """}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        result = response.choices[0].message.content
        return parse_llm_response(result)
        
    except Exception as e:
        logger.error(f"Error in label generation: {str(e)}")
        return []

@app.get("/")
async def root():
    """ルートパスへのアクセスを/docsにリダイレクト"""
    return RedirectResponse(url="/docs")

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化処理"""
    if ENV == "development":
        try:
            # ngrokのトンネルを設定
            public_url = ngrok.connect(PORT)
            logger.info(f'Public URL: {public_url.public_url}')
        except Exception as e:
            logger.error(f"Failed to start ngrok: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    if ENV == "development":
        ngrok.kill()

# ヘルスチェック用のエンドポイント
@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "environment": ENV,
        "gitlab_url": GITLAB_URL
    }

def log_webhook_event(event: Dict):
    """
    Webhookイベントの内容を詳細にログに記録する
    """
    logger.info("======= GitLab Webhook Event Details =======")
    logger.info(f"Event Type: {event.get('object_kind')}")
    logger.info(f"Event created at: {event.get('created_at')}")
    
    # プロジェクト情報
    project = event.get('project', {})
    logger.info("\n=== Project Information ===")
    logger.info(f"Project ID: {project.get('id')}")
    logger.info(f"Project Name: {project.get('name')}")
    logger.info(f"Project Path: {project.get('path_with_namespace')}")
    logger.info(f"Project URL: {project.get('web_url')}")
    
    # オブジェクト属性
    attrs = event.get('object_attributes', {})
    logger.info("\n=== Object Attributes ===")
    logger.info(f"ID: {attrs.get('id')}")
    logger.info(f"IID: {attrs.get('iid')}")
    logger.info(f"Title: {attrs.get('title')}")
    logger.info(f"Description: {attrs.get('description')}")
    logger.info(f"State: {attrs.get('state')}")
    logger.info(f"URL: {attrs.get('url')}")
    logger.info(f"Action: {attrs.get('action')}")
    logger.info(f"Created At: {attrs.get('created_at')}")
    logger.info(f"Updated At: {attrs.get('updated_at')}")
    
    # ユーザー情報
    user = event.get('user', {})
    logger.info("\n=== User Information ===")
    logger.info(f"User ID: {user.get('id')}")
    logger.info(f"Username: {user.get('username')}")
    logger.info(f"Name: {user.get('name')}")
    
    # ラベル情報
    labels = event.get('labels', [])
    if labels:
        logger.info("\n=== Labels ===")
        for label in labels:
            logger.info(f"- {label.get('title')} ({label.get('color')})")
    
    # 変更情報
    changes = event.get('changes', {})
    if changes:
        logger.info("\n=== Changes ===")
        for key, value in changes.items():
            logger.info(f"{key}: {value}")
            
    logger.info("==========================================\n")

# Webhookエンドポイント
@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    GitLabからのWebhookを処理するエンドポイント
    """
    # GitLabからのシークレットトークンを検証
    gitlab_token = request.headers.get("X-Gitlab-Token")
    if gitlab_token != WEBHOOK_SECRET:
        logger.warning("Invalid webhook token received")
        raise HTTPException(status_code=401, detail="Invalid webhook token")
    
    try:
        event = await request.json()
        
        # イベントの詳細をログに記録
        log_webhook_event(event)
        
        # issueイベント以外は無視
        if event.get('object_kind') != 'issue':
            logger.info(f"Skipping non-issue event: {event.get('object_kind')}")
            return {
                "status": "skipped",
                "message": "Not an issue event",
                "event_type": event.get('object_kind')
            }
            
        # issueの内容を取得
        project_id = event['project']['id']
        issue_iid = event['object_attributes']['iid']
        title = event['object_attributes']['title']
        description = event['object_attributes']['description'] or ''
        
        # プロジェクトとissueの取得
        gl = get_gitlab_client()
        project = gl.projects.get(project_id)
        issue = project.issues.get(issue_iid)
        
        # LLMを使用してラベルを取得
        labels_to_add = get_labels_from_llm(title, description)
        logger.info(f"LLM suggested labels: {labels_to_add}")
        
        # 既存のラベルを保持しつつ、新しいラベルを追加
        current_labels = issue.labels
        new_labels = list(set(current_labels + labels_to_add))
        
        # ラベルの更新
        if labels_to_add:
            issue.labels = new_labels
            issue.save()
            logger.info(f"Updated labels for issue #{issue_iid}: {new_labels}")
            
        return {
            "status": "success",
            "issue_id": issue_iid,
            "added_labels": labels_to_add,
            "current_labels": new_labels,
            "event_details": event
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
