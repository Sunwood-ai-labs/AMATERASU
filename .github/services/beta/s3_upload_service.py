import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boto3
from botocore.exceptions import NoCredentialsError
from loguru import logger
from config import get_settings

class S3UploadService:
    def __init__(self):
        self.settings = get_settings()
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
                                      region_name=self.settings.AWS_REGION)
        self.bucket_name = self.settings.S3_BUCKET_NAME
        self.repo_owner, self.repo_name = self.settings.GITHUB_REPOSITORY.split('/')

    def upload_file_to_s3(self, file_path, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_path)

        s3_object_key = f"{self.repo_owner}/{self.repo_name}/{object_name}"

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_object_key)
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_object_key}"
            logger.info(f"ファイルが正常にアップロードされました。S3 URL: {s3_url}")
            return s3_url
        except FileNotFoundError:
            logger.error(f"ファイル {file_path} が見つかりません")
            return None
        except NoCredentialsError:
            logger.error("認証情報が利用できません")
            return None
        except Exception as e:
            logger.error(f"ファイルのアップロード中にエラーが発生しました: {str(e)}")
            return None

    def get_s3_url(self, object_name):
        s3_object_key = f"{self.repo_owner}/{self.repo_name}/{object_name}"
        return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_object_key}"

if __name__ == "__main__":
    logger.info("S3アップロードサービスのテストを開始します")

    from dotenv import load_dotenv
    dotenv_path=os.path.join(os.getcwd(), '.env')
    logger.debug(f"dotenv_path : {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)

    # S3UploadServiceのインスタンスを作成
    s3_service = S3UploadService()

    # テスト用のファイルパスを設定
    # 注意: このパスは実際のファイルパスに置き換えてください
    test_file_path = r".github\release_notes\header_image\release_header_v1.0.0.png"
    test_object_name = "release_header_v1.0.0.png"

    # ファイルをアップロード
    upload_url = s3_service.upload_file_to_s3(test_file_path, test_object_name)

    if upload_url:
        logger.info(f"ファイルが正常にアップロードされました。URL: {upload_url}")

        # アップロードしたファイルのURLを取得
        retrieved_url = s3_service.get_s3_url(test_object_name)
        logger.info(f"アップロードされたファイルの取得URL: {retrieved_url}")

        # URLが一致することを確認
        if upload_url == retrieved_url:
            logger.info("アップロードURLと取得URLが一致しました。テスト成功。")
        else:
            logger.error("URLが一致しません。テスト失敗。")
    else:
        logger.error("ファイルのアップロードに失敗しました。テスト失敗。")

    logger.info("S3アップロードサービスのテストが完了しました")
