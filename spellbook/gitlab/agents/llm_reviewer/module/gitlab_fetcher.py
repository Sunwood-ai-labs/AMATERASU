from typing import Dict, Optional
import gitlab
import os
from datetime import datetime
from dataclasses import dataclass
from loguru import logger

@dataclass
class MergeRequestData:
    title: str
    description: str
    diff: str
    state: str
    author: str
    created_at: str
    web_url: str
    project_id: str
    mr_iid: int

class GitLabFetcher:
    def __init__(self, url: str, token: str):
        self.client = gitlab.Gitlab(url, private_token=token)
        
    def get_merge_request(self, project_id: str, mr_iid: int) -> MergeRequestData:
        """マージリクエストの詳細を取得"""
        try:
            project = self.client.projects.get(project_id)
            mr = project.mergerequests.get(mr_iid)
            
            # 差分の取得
            changes = mr.changes()
            diff_content = []
            for change in changes['changes']:
                diff_content.append(f"File: {change['new_path']}\n{change['diff']}")
            
            return MergeRequestData(
                title=mr.title,
                description=mr.description or "",
                diff="\n\n".join(diff_content),
                state=mr.state,
                author=mr.author['username'],
                created_at=mr.created_at,
                web_url=mr.web_url,
                project_id=project_id,
                mr_iid=mr_iid
            )
            
        except Exception as e:
            logger.error(f"Failed to fetch merge request: {e}")
            raise

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    
    # 環境変数の読み込み
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='GitLab MR Fetcher')
    parser.add_argument('--project-id', required=True, help='GitLab project ID')
    parser.add_argument('--mr-iid', required=True, type=int, help='Merge request IID')
    args = parser.parse_args()
    
    # フェッチャーの初期化
    fetcher = GitLabFetcher(
        url=os.getenv("GITLAB_URL", "http://gitlab.example.com"),
        token=os.getenv("GITLAB_TOKEN")
    )
    
    # MRの取得と表示
    try:
        mr_data = fetcher.get_merge_request(args.project_id, args.mr_iid)
        print("\n=== Merge Request Details ===")
        print(f"Title: {mr_data.title}")
        print(f"Author: {mr_data.author}")
        print(f"State: {mr_data.state}")
        print(f"URL: {mr_data.web_url}")
        print("\n=== Diff Preview ===")
        print(mr_data.diff[:500] + "..." if len(mr_data.diff) > 500 else mr_data.diff)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)