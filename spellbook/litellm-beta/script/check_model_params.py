from litellm import get_supported_openai_params
from loguru import logger
import sys
from typing import List, Tuple, Optional

# モデルとプロバイダーの定義
class ModelInfo:
    def __init__(self, name: str, provider: Optional[str], description: str):
        self.name = name
        self.provider = provider
        self.description = description

# チェックするモデルのリスト
models_to_check: List[ModelInfo] = [
    # Claude 3.5 Family
    ModelInfo("claude-3-5-sonnet-20241022", "anthropic", "Claude 3.5 Sonnet (Anthropic API)"),
    ModelInfo("anthropic.claude-3-5-sonnet-20241022-v2:0", "bedrock", "Claude 3.5 Sonnet (AWS Bedrock)"),
    ModelInfo("claude-3-5-sonnet-v2@20241022", "vertex_ai", "Claude 3.5 Sonnet (GCP Vertex AI)"),
    ModelInfo("claude-3-5-haiku-20241022", "anthropic", "Claude 3.5 Haiku (Anthropic API)"),
    ModelInfo("anthropic.claude-3-5-haiku-20241022-v1:0", "bedrock", "Claude 3.5 Haiku (AWS Bedrock)"),
    ModelInfo("claude-3-5-haiku@20241022", "vertex_ai", "Claude 3.5 Haiku (GCP Vertex AI)"),

    # Claude 3 Family
    ModelInfo("claude-3-opus-20240229", "anthropic", "Claude 3 Opus (Anthropic API)"),
    ModelInfo("anthropic.claude-3-opus-20240229-v1:0", "bedrock", "Claude 3 Opus (AWS Bedrock)"),
    ModelInfo("claude-3-opus@20240229", "vertex_ai", "Claude 3 Opus (GCP Vertex AI)"),
    ModelInfo("claude-3-sonnet-20240229", "anthropic", "Claude 3 Sonnet (Anthropic API)"),
    ModelInfo("anthropic.claude-3-sonnet-20240229-v1:0", "bedrock", "Claude 3 Sonnet (AWS Bedrock)"),
    ModelInfo("claude-3-sonnet@20240229", "vertex_ai", "Claude 3 Sonnet (GCP Vertex AI)"),
    ModelInfo("claude-3-haiku-20240307", "anthropic", "Claude 3 Haiku (Anthropic API)"),
    ModelInfo("anthropic.claude-3-haiku-20240307-v1:0", "bedrock", "Claude 3 Haiku (AWS Bedrock)"),
    ModelInfo("claude-3-haiku@20240307", "vertex_ai", "Claude 3 Haiku (GCP Vertex AI)"),

    # OpenAI Models
    ModelInfo("gpt-4-0125-preview", None, "GPT-4 Turbo Preview"),
    ModelInfo("gpt-4-1106-preview", None, "GPT-4 Turbo Preview (Previous)"),
    ModelInfo("gpt-4-vision-preview", None, "GPT-4 Vision"),
    ModelInfo("gpt-4", None, "GPT-4 Base"),
    ModelInfo("gpt-3.5-turbo-0125", None, "GPT-3.5 Turbo Latest"),
    ModelInfo("gpt-3.5-turbo-1106", None, "GPT-3.5 Turbo (Previous)"),

    # Google Models
    ModelInfo("gemini-pro", "google", "Gemini Pro"),
    ModelInfo("gemini-pro-vision", "google", "Gemini Pro Vision"),
    ModelInfo("gemini-ultra", "google", "Gemini Ultra"),
    
    # Anthropic Legacy Models
    ModelInfo("claude-2.1", "anthropic", "Claude 2.1"),
    ModelInfo("claude-2.0", "anthropic", "Claude 2.0"),
    
    # Mistral Models
    ModelInfo("mistral-tiny", "mistral", "Mistral Tiny"),
    ModelInfo("mistral-small", "mistral", "Mistral Small"),
    ModelInfo("mistral-medium", "mistral", "Mistral Medium"),
    ModelInfo("mistral-large", "mistral", "Mistral Large"),

    # Azure OpenAI
    ModelInfo("gpt-4", "azure", "Azure GPT-4"),
    ModelInfo("gpt-35-turbo", "azure", "Azure GPT-3.5 Turbo"),
]

def main():
    logger.info("Starting comprehensive parameter support check for models")

    for model_info in models_to_check:
        try:
            logger.info("=" * 80)
            logger.info(f"Checking: {model_info.description}")
            logger.info(f"Model ID: {model_info.name}")
            logger.info(f"Provider: {model_info.provider if model_info.provider else 'OpenAI'}")
            
            params = get_supported_openai_params(
                model=model_info.name, 
                custom_llm_provider=model_info.provider
            )
            
            # パラメータをカテゴリ別に整理
            param_categories = {
                "Core": ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"],
                "Response Format": ["response_format", "seed", "tools", "tool_choice"],
                "Other": []
            }
            
            for param in params:
                categorized = False
                for category, category_params in param_categories.items():
                    if param in category_params:
                        categorized = True
                        break
                if not categorized:
                    param_categories["Other"].append(param)
            
            logger.success(f"Found {len(params)} supported parameters")
            
            # カテゴリ別にパラメータを表示
            for category, category_params in param_categories.items():
                if category_params:
                    logger.info(f"\n{category} Parameters:")
                    for param in category_params:
                        if param in params:
                            logger.debug(f"└─ {param}")
            
        except Exception as e:
            logger.error(f"Error checking {model_info.name}: {str(e)}")
        
        logger.debug("-" * 80)

    logger.info("Parameter support check completed")

if __name__ == "__main__":
    main()
