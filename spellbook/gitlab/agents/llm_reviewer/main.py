import argparse
import os
from dotenv import load_dotenv
from loguru import logger
from module.gitlab_fetcher import GitLabFetcher
from module.llm_analyzer import LLMAnalyzer
from module.gitlab_commenter import GitLabCommenter

def get_available_models():
    """利用可能なモデルのリストを返す"""
    return [
        "gpt-4o",
        "gpt-3.5-turbo",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "anthropic/claude-3-opus-20240229",
        "anthropic/claude-3-sonnet-20240229",
        "bedrock/anthropic.claude-3-sonnet-20240229",
        "bedrock/anthropic.claude-3-haiku-20240307"
    ]

def main():
    # 環境変数の読み込み
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='GitLab MR Review Pipeline')
    parser.add_argument('--project-id', required=True, help='GitLab project ID')
    parser.add_argument('--mr-iid', required=True, type=int, help='Merge request IID')
    parser.add_argument('--output-dir', default='outputs', help='Directory to save analysis results')
    parser.add_argument('--skip-comment', action='store_true', help='Skip posting comment to GitLab')
    parser.add_argument('--model', 
                      default='gpt-4o',
                      choices=get_available_models(),
                      help='LLM model to use for analysis')
    parser.add_argument('--temperature',
                      type=float,
                      default=0.3,
                      help='Temperature for LLM inference (0.0-1.0)')
    parser.add_argument('--max-tokens',
                      type=int,
                      default=2000,
                      help='Maximum tokens for LLM response')
    args = parser.parse_args()
    
    try:
        # GitLabからMRを取得
        logger.info("Fetching merge request details...")
        fetcher = GitLabFetcher(
            url=os.getenv("GITLAB_URL", "http://gitlab.example.com"),
            token=os.getenv("GITLAB_TOKEN")
        )
        mr_data = fetcher.get_merge_request(args.project_id, args.mr_iid)
        logger.info(f"Successfully fetched MR: {mr_data.title}")
        
        # LLMで分析
        logger.info(f"Analyzing with LLM (model: {args.model}, temperature: {args.temperature})...")
        analyzer = LLMAnalyzer(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_base=os.getenv("API_BASE", "https://api.openai.com/v1"),
            output_dir=args.output_dir,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        review_result = analyzer.analyze(mr_data)
        logger.info(f"Analysis complete. Overall rating: {review_result.overall_rating}/5")
        
        # GitLabにコメント投稿（オプション）
        if not args.skip_comment:
            logger.info("Posting review comment to GitLab...")
            commenter = GitLabCommenter(
                url=os.getenv("GITLAB_URL", "http://gitlab.example.com"),
                token=os.getenv("GITLAB_TOKEN")
            )
            success = commenter.post_comment(args.project_id, args.mr_iid, review_result)
            if success:
                logger.info("Successfully posted review comment!")
            else:
                logger.error("Failed to post review comment")
                return 1
        
        logger.info("Review process completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error in review process: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
