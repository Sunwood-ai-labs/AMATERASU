# add_claude_model_definition.py

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import json
from loguru import logger
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
            logger.info(f"Creating model definition with payload: {json.dumps(payload, indent=2)}")
            response = requests.post(
                f"{self.base_url}/api/public/models",
                auth=self.auth,
                json=payload
            )
            response.raise_for_status()
            logger.info(f"Successfully created model definition for {model_name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create model: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
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
            logger.error(f"Failed to get models: {str(e)}")
            raise

def configure_claude_models(creator):
    """Configure all Claude model definitions with updated patterns."""
    
    # Claude 3.5 Haiku 20241022
    creator.create_model(
        model_name="claude-3.5-haiku-20241022",
        match_pattern=r"(?i)^(.*[/])?claude-3-5-haiku-20241022(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000001,  # $0.001/1K tokens
        output_price=0.000005,  # $0.005/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3.5 Haiku Latest
    creator.create_model(
        model_name="claude-3.5-haiku-latest",
        match_pattern=r"(?i)^(.*[/])?claude-3-5-haiku-latest(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000001,  # $0.001/1K tokens
        output_price=0.000005,  # $0.005/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3.5 Sonnet 20240620
    creator.create_model(
        model_name="claude-3.5-sonnet-20240620",
        match_pattern=r"(?i)^(.*[/])?claude-3-5-sonnet-20240620(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000003,  # $0.003/1K tokens
        output_price=0.000015,  # $0.015/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3.5 Sonnet 20241022
    creator.create_model(
        model_name="claude-3.5-sonnet-20241022",
        match_pattern=r"(?i)^(.*[/])?claude-3-5-sonnet-20241022(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000003,  # $0.003/1K tokens
        output_price=0.000015,  # $0.015/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3.5 Sonnet Latest
    creator.create_model(
        model_name="claude-3.5-sonnet-latest",
        match_pattern=r"(?i)^(.*[/])?claude-3-5-sonnet-latest(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000003,  # $0.003/1K tokens
        output_price=0.000015,  # $0.015/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3 Haiku 20240307
    creator.create_model(
        model_name="claude-3-haiku-20240307",
        match_pattern=r"(?i)^(.*[/])?claude-3-haiku-20240307(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.00000025,  # $0.00025/1K tokens
        output_price=0.00000125,  # $0.00125/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3 Opus 20240229
    creator.create_model(
        model_name="claude-3-opus-20240229",
        match_pattern=r"(?i)^(.*[/])?claude-3-opus-20240229(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000015,  # $0.015/1K tokens
        output_price=0.000075,  # $0.075/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

    # Claude 3 Sonnet 20240229
    creator.create_model(
        model_name="claude-3-sonnet-20240229",
        match_pattern=r"(?i)^(.*[/])?claude-3-sonnet-20240229(-[a-zA-Z]+\d+)?$",
        unit="TOKENS",
        input_price=0.000003,  # $0.003/1K tokens
        output_price=0.000015,  # $0.015/1K tokens
        tokenizer_id="claude",
        tokenizer_config={"type": "claude"}
    )

def main():
    # Langfuse認証情報
    PUBLIC_KEY = "pk-lf-da6122ed-870b-4582-ad68-932a37868e6f"
    SECRET_KEY = "sk-lf-a352a740-f507-4554-8dac-53d6c36fadc0"
    
    try:
        creator = LangfuseModelCreator(
            public_key=PUBLIC_KEY,
            secret_key=SECRET_KEY,
            base_url="https://amaterasu-langfuse-dev.sunwood-ai-labs.click"
        )
        
        # 既存のモデル定義を確認
        logger.info("Fetching existing model definitions...")
        existing_models = creator.get_models()
        logger.info(f"Found {len(existing_models.get('data', []))} existing model definitions")
        
        configure_claude_models(creator)
        
        
        logger.success("---------------------")        
        logger.success("Model definition created successfully:")

        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
