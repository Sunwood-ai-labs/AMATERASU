from litellm import get_supported_openai_params
from loguru import logger
import sys
from typing import List, Optional

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
    logger.info("Starting JSON support check for models")
    logger.info("Checking which models support response_format/json_schema")

    # 結果を保存するための辞書
    results = {
        "json_supported": [],
        "json_not_supported": [],
        "error": []
    }

    for model_info in models_to_check:
        try:
            params = get_supported_openai_params(
                model=model_info.name, 
                custom_llm_provider=model_info.provider
            )
            
            model_display = f"{model_info.description} ({model_info.provider if model_info.provider else 'OpenAI'})"
            
            # response_formatパラメータのサポートを確認
            if "response_format" in params:
                results["json_supported"].append(model_display)
                logger.success(f"✅ {model_display} - JSON Supported")
            else:
                results["json_not_supported"].append(model_display)
                logger.warning(f"❌ {model_display} - JSON Not Supported")
            
        except Exception as e:
            results["error"].append(model_display)
            logger.error(f"⚠️ {model_display} - Error: {str(e)}")

    # サマリーの表示
    logger.info("" + "="*50)
    logger.info("Summary Report")
    logger.info("="*50)
    
    logger.info(f"\nModels with JSON Support ({len(results['json_supported'])}): ")
    for model in results['json_supported']:
        logger.info(f"✅ {model}")
    
    logger.info(f"\nModels without JSON Support ({len(results['json_not_supported'])}): ")
    for model in results['json_not_supported']:
        logger.info(f"❌ {model}")
    
    if results["error"]:
        logger.info(f"\nModels with Errors ({len(results['error'])}): ")
        for model in results['error']:
            logger.info(f"⚠️ {model}")

    logger.info("\nCheck completed!")

if __name__ == "__main__":
    main()
