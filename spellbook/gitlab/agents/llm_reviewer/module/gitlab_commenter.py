from typing import Optional
import gitlab
from loguru import logger
from .llm_analyzer import ReviewResult

class GitLabCommenter:
    def __init__(self, url: str, token: str):
        self.client = gitlab.Gitlab(url, private_token=token)
        
    def format_comment(self, review: ReviewResult) -> str:
        """レビュー結果をマークダウン形式でフォーマット"""
        return f"""## LLMによるマージリクエストレビュー結果

### 評価スコア
|カテゴリ|スコア (1-5)|
|---|:---:|
|コード品質|{review.code_quality['rating']}|
|セキュリティ|{review.security_evaluation['rating']}|
|テスト|{review.testing_assessment['rating']}|
|アーキテクチャ|{review.architecture_review['rating']}|
|総合評価|{review.overall_rating}|

### コード品質
**長所:**
{chr(10).join(f'- {s}' for s in review.code_quality['strengths'])}

**短所:**
{chr(10).join(f'- {w}' for w in review.code_quality['weaknesses'])}

### セキュリティ評価
{chr(10).join(f'⚠️ {c}' for c in review.security_evaluation['concerns'])}

### 改善提案
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(review.improvement_suggestions))}

### 総評
{review.summary}"""
        
    def post_comment(self, project_id: str, mr_iid: int, review: ReviewResult) -> bool:
        """マージリクエストにコメントを投稿"""
        try:
            project = self.client.projects.get(project_id)
            mr = project.mergerequests.get(mr_iid)
            comment = self.format_comment(review)
            mr.notes.create({'body': comment})
            logger.info(f"Successfully posted review comment to MR !{mr_iid}")
            return True
        except Exception as e:
            logger.error(f"Failed to post comment: {e}")
            return False

if __name__ == "__main__":
    import argparse
    import json
    from dotenv import load_dotenv
    import os
    
    # 環境変数の読み込み
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='GitLab MR Commenter')
    parser.add_argument('--project-id', required=True, help='GitLab project ID')
    parser.add_argument('--mr-iid', required=True, type=int, help='Merge request IID')
    parser.add_argument('--analysis-file', required=True, help='Path to analysis result JSON file')
    args = parser.parse_args()
    
    # 分析結果の読み込み
    try:
        with open(args.analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # ReviewResultオブジェクトの作成
        result_dict = analysis_data['review_result']
        result = ReviewResult(
            code_quality=result_dict['code_quality'],
            security_evaluation=result_dict['security_evaluation'],
            testing_assessment=result_dict['testing_assessment'],
            architecture_review=result_dict['architecture_review'],
            improvement_suggestions=result_dict['improvement_suggestions'],
            overall_rating=result_dict['overall_rating'],
            summary=result_dict['summary'],
            raw_response=result_dict
        )
        
        # コメントの投稿
        commenter = GitLabCommenter(
            url=os.getenv("GITLAB_URL", "http://gitlab.example.com"),
            token=os.getenv("GITLAB_TOKEN")
        )
        
        success = commenter.post_comment(args.project_id, args.mr_iid, result)
        if success:
            print("Successfully posted the review comment!")
        else:
            print("Failed to post the review comment.")
            exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)