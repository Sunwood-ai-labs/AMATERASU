# add_claude_model_definition.py

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import json
import logging
import sys

class LangfuseModelCreator:
    def __init__(self, public_key: str, secret_key: str, base_url: str = "http://localhost:3000"):
        """
        Initialize the LangfuseModelCreator
        
        Args:
            public_key: Langfuse Public Key
            secret_key: Langfuse Secret Key
            base_url: Base URL for Langfuse API (defaults to local instance)
        """
        self.auth = (public_key, secret_key)
        self.base_url = base_url.rstrip('/')
        
    def create_model(self,
                    model_name: str,
                    match_pattern: str,
                    unit: str,
                    input_price: Optional[float] = None,
                    output_price: Optional[float] = None,
                    total_price: Optional[float] = None,
                    start_date: Optional[datetime] = None,
                    tokenizer_id: Optional[str] = None,
                    tokenizer_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new model definition in Langfuse
        """
        if total_price is not None and (input_price is not None or output_price is not None):
            raise ValueError("Cannot specify both total_price and input/output prices")
            
        payload = {
            "modelName": model_name,
            "matchPattern": match_pattern,
            "unit": unit,
            "inputPrice": input_price,
            "outputPrice": output_price,
            "totalPrice": total_price,
        }
        
        if start_date:
            payload["startDate"] = start_date.isoformat()
        if tokenizer_id:
            payload["tokenizerId"] = tokenizer_id
        if tokenizer_config:
            payload["tokenizerConfig"] = tokenizer_config
            
        try:
            logging.info(f"Creating model definition with payload: {json.dumps(payload, indent=2)}")
            response = requests.post(
                f"{self.base_url}/api/public/models",
                auth=self.auth,
                json=payload
            )
            response.raise_for_status()
            logging.info(f"Successfully created model definition for {model_name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create model: {str(e)}")
            if hasattr(e.response, 'text'):
                logging.error(f"Response content: {e.response.text}")
            raise

    def get_models(self) -> Dict[str, Any]:
        """Get all existing model definitions"""
        try:
            response = requests.get(
                f"{self.base_url}/api/public/models",
                auth=self.auth
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get models: {str(e)}")
            raise

def main():
    # Langfuse認証情報
    PUBLIC_KEY = "pk-lf-faccb782-2b76-4750-ac9b-f83b2be90ff1"
    SECRET_KEY = "sk-lf-4e26deec-2e04-4a16-8aa2-21c94853e83e"
    
    try:
        creator = LangfuseModelCreator(
            public_key=PUBLIC_KEY,
            secret_key=SECRET_KEY
        )
        
        # 既存のモデル定義を確認
        logging.info("Fetching existing model definitions...")
        existing_models = creator.get_models()
        logging.info(f"Found {len(existing_models.get('data', []))} existing model definitions")
        
        # Claude 3.5 Sonnet 20240620のモデル定義を作成
        claude_model = creator.create_model(
            model_name="claude-3.5-sonnet-20240620",
            # 前方に任意のプレフィックスがあり、末尾に-US1などのリージョン指定がオプショナルなパターンにマッチ
            match_pattern=r"(?i)^(.*[/])?claude-3-5-sonnet-20240620(-[a-zA-Z]+\d+)?$",
            unit="TOKENS",
            input_price=0.000003,  # $0.003/1K tokens
            output_price=0.000015,  # $0.015/1K tokens
            tokenizer_id="claude",
            tokenizer_config={
                "type": "claude"
            }
        )
        
        logging.info("Model definition created successfully:")
        logging.info(json.dumps(claude_model, indent=2))
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
