import openai
from loguru import logger
import sys
import time
from art import text2art

def print_banner():
    """アプリケーションバナーを表示"""
    art = text2art("Bedrock Nova", font='rnd-large')
    logger.info("\n\033[94m" + art + "\033[0m")
    logger.info("\033[92m" + "=" * 50 + "\033[0m")
    logger.info("\033[93mBedrock Nova Models Testing Tool\033[0m")
    logger.info("\033[92m" + "=" * 50 + "\033[0m\n")

class BedrockTester:
    def __init__(self, base_url="http://localhost:4000"):
        """初期化
        Args:
            base_url (str): LiteLLM サーバーのベースURL
        """
        self.client = openai.OpenAI(
            api_key="sk-1234",  # LiteLLM用のダミーキー
            base_url=base_url
        )
        logger.info(f"OpenAI クライアントを初期化: {base_url}")
        
        self.models = [
            "bedrock/nova-micro",
            "bedrock/nova-lite",
            "bedrock/nova-pro"
        ]
        self.test_messages = [
            {
                "role": "user",
                "content": "日本の四季について短く説明してください。"
            }
        ]

    def test_model(self, model_name: str):
        """各モデルをテストする関数"""
        try:
            logger.info(f"{model_name} のテストを開始します")
            start_time = time.time()

            response = self.client.chat.completions.create(
                model=model_name,
                messages=self.test_messages,
                temperature=0.7,
                max_tokens=500
            )

            response_time = time.time() - start_time
            
            logger.success(f"{model_name} のテストが成功しました")
            logger.info(f"応答時間: {response_time:.2f}秒")
            logger.info(f"応答内容:\n{response.choices[0].message.content}")
            logger.info(f"使用トークン数: {response.usage.total_tokens}")
            
            return True

        except Exception as e:
            logger.error(f"{model_name} のテスト中にエラーが発生しました: {str(e)}")
            return False

    def run_all_tests(self):
        """全モデルのテストを実行する"""
        logger.info("Bedrock Novaモデルのテストを開始します")
        
        for model in self.models:
            success = self.test_model(model)
            if success:
                logger.info(f"{model}: テスト成功 ✅")
            else:
                logger.error(f"{model}: テスト失敗 ❌")
            
            # モデル間で少し待機
            time.sleep(2)

def main():
    """メイン実行関数"""
    try:
        # バナーを表示
        print_banner()
        
        # LiteLLMサーバーのURLを指定
        base_url = "http://localhost:4000"  # 必要に応じてURLを変更
        
        tester = BedrockTester(base_url=base_url)
        tester.run_all_tests()
        
    except Exception as e:
        logger.critical(f"予期せぬエラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
