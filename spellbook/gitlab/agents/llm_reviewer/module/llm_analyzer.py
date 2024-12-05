import openai
import json
import os
from typing import Dict
from datetime import datetime
from dataclasses import dataclass
from loguru import logger
from .gitlab_fetcher import MergeRequestData

@dataclass
class ReviewResult:
    code_quality: Dict
    security_evaluation: Dict
    testing_assessment: Dict
    architecture_review: Dict
    improvement_suggestions: list
    overall_rating: int
    summary: str
    raw_response: Dict

class LLMAnalyzer:
    def __init__(self, api_key: str, api_base: str, output_dir: str, 
                 model: str = "gpt-4", temperature: float = 0.3, 
                 max_tokens: int = 2000):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        self.output_dir = output_dir
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        os.makedirs(output_dir, exist_ok=True)
        
    def save_analysis(self, mr_data: MergeRequestData, result: ReviewResult) -> str:
        """分析結果を保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{mr_data.project_id}_{mr_data.mr_iid}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'project_id': mr_data.project_id,
                    'mr_iid': mr_data.mr_iid,
                    'timestamp': timestamp,
                    'model': self.model,
                    'temperature': self.temperature
                },
                'merge_request': {
                    'title': mr_data.title,
                    'description': mr_data.description,
                    'author': mr_data.author,
                    'created_at': mr_data.created_at
                },
                'review_result': result.raw_response
            }, f, ensure_ascii=False, indent=2)
        
        return filepath
        
    def analyze(self, mr_data: MergeRequestData) -> ReviewResult:
        """LLMを使用してマージリクエストを分析"""
        try:
            # プロンプトの読み込み
            prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "review_prompt.txt")
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"""
                    Title: {mr_data.title}
                    Description: {mr_data.description}
                    
                    Changes:
                    {mr_data.diff}
                    """}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result_dict = json.loads(response.choices[0].message.content)
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
            
            # 分析結果を保存
            saved_path = self.save_analysis(mr_data, result)
            logger.info(f"Analysis result saved to: {saved_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze merge request: {e}")
            raise

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    from gitlab_fetcher import GitLabFetcher
    
    # 環境変数の読み込み
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='LLM Analyzer for GitLab MR')
    parser.add_argument('--project-id', required=True, help='GitLab project ID')
    parser.add_argument('--mr-iid', required=True, type=int, help='Merge request IID')
    parser.add_argument('--output-dir', default='outputs', help='Directory to save analysis results')
    parser.add_argument('--model', default='gpt-4', help='LLM model to use')
    parser.add_argument('--temperature', type=float, default=0.3, help='Temperature for LLM')
    parser.add_argument('--max-tokens', type=int, default=2000, help='Max tokens for LLM response')
    args = parser.parse_args()
    
    # MRの取得
    fetcher = GitLabFetcher(
        url=os.getenv("GITLAB_URL", "http://gitlab.example.com"),
        token=os.getenv("GITLAB_TOKEN")
    )
    mr_data = fetcher.get_merge_request(args.project_id, args.mr_iid)
    
    # LLM分析の実行
    analyzer = LLMAnalyzer(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_base=os.getenv("API_BASE", "https://api.openai.com/v1"),
        output_dir=args.output_dir,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    
    try:
        result = analyzer.analyze(mr_data)
        print("\n=== Analysis Result ===")
        print(f"Model: {args.model}")
        print(f"Temperature: {args.temperature}")
        print(f"Overall Rating: {result.overall_rating}/5")
        print(f"\nCode Quality Rating: {result.code_quality['rating']}/5")
        print(f"Security Rating: {result.security_evaluation['rating']}/5")
        print(f"Testing Rating: {result.testing_assessment['rating']}/5")
        print(f"Architecture Rating: {result.architecture_review['rating']}/5")
        print("\nSummary:")
        print(result.summary)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)