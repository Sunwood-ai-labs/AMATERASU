import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import subprocess
from loguru import logger
from config import get_settings

class GitHubCDNService:
    def __init__(self):
        self.settings = get_settings()
        self.repo = self.settings.GITHUB_REPOSITORY
        logger.info(f"GitHubCDNService initialized with repo: {self.repo}")

    def run_command(self, command):
        logger.info(f"実行するコマンド: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f"コマンド出力: {result.stdout.strip()}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"コマンド実行エラー: {e.stderr}")
            logger.error(f"エラーコード: {e.returncode}")
            return None

    def upload_to_github_cdn(self, file_path):
        logger.info(f"GitHubCDNにファイルをアップロード: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"ファイルが見つかりません: {file_path}")
            return None
        
        # リポジトリIDの取得
        repo_info_cmd = ["gh", "api", f"/repos/{self.repo}"]
        repo_info = self.run_command(repo_info_cmd)
        if not repo_info:
            logger.error("リポジトリ情報の取得に失敗しました")
            return None
        
        repo_id = json.loads(repo_info)["id"]
        
        # リリースID (例: v1.0.0)
        release_id = "v1.9.1" 

        # 画像をアップロード
        upload_url = f"https://uploads.github.com/repos/{self.repo}/releases/assets/{release_id}"
        
        logger.info(f"アップロードURL: {upload_url}")
        
        file_name = os.path.basename(file_path)
        curl_cmd = [
            "curl",
            "-X", "POST",
            "-H", f"Authorization: token {self.settings.GITHUB_TOKEN}",
            "-H", "Content-Type: application/octet-stream",
            "-H", f"Content-Length: {os.path.getsize(file_path)}",
            "--data-binary", f"@{file_path}",
            f"{upload_url}?name={file_name}"
        ]
        curl_result = self.run_command(curl_cmd)
        if not curl_result:
            logger.error("curlコマンドの実行に失敗しました")
            return None

        try:
            response = json.loads(curl_result)
            image_url = response.get('browser_download_url')
            logger.info(f"解析されたレスポンス: {response}")
        except json.JSONDecodeError:
            logger.error(f"JSONの解析に失敗しました。curl_result: {curl_result}")
            return None

        logger.info(f"GitHubCDNにアップロードされた画像URL: {image_url}")
        return image_url

    def get_cdn_url(self, file_name):
        return f"https://raw.githubusercontent.com/{self.repo}/main/docs/release_notes/header_image/{file_name}"

if __name__ == "__main__":
    logger.info("GitHubCDNサービスのテストを開始します")

    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.getcwd(), '.env')
    logger.debug(f"dotenv_path : {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)

    cdn_service = GitHubCDNService()
    test_file_path = "docs/release_notes/header_image/release_header_v1.0.0.png"
    
    logger.info(f"テスト対象ファイル: {test_file_path}")
    logger.info(f"ファイルの存在: {os.path.exists(test_file_path)}")
    
    uploaded_url = cdn_service.upload_to_github_cdn(test_file_path)
    if uploaded_url:
        logger.info(f"ファイルが正常にアップロードされました。URL: {uploaded_url}")
    else:
        logger.error("ファイルのアップロードに失敗しました。")

    logger.info("GitHubCDNサービスのテストが完了しました")
