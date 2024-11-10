import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boto3
from botocore.exceptions import ClientError
from loguru import logger
import json
from config import get_settings

class S3PublicAccessSetup:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def set_public_read_policy(self):
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                }
            ]
        }

        policy_string = json.dumps(bucket_policy)

        try:
            self.s3_client.put_bucket_policy(Bucket=self.bucket_name, Policy=policy_string)
            logger.info(f"バケット {self.bucket_name} に公開読み取りポリシーを設定しました。")
        except ClientError as e:
            logger.error(f"バケットポリシーの設定中にエラーが発生しました: {e}")

    def enable_public_access(self):
        try:
            self.s3_client.put_public_access_block(
                Bucket=self.bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            logger.info(f"バケット {self.bucket_name} のパブリックアクセスブロックを無効化しました。")
        except ClientError as e:
            logger.error(f"パブリックアクセスブロックの設定中にエラーが発生しました: {e}")

if __name__ == "__main__":
    
    from dotenv import load_dotenv
    dotenv_path=os.path.join(os.getcwd(), '.env')
    logger.debug(f"dotenv_path : {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)
    
    settings = get_settings()
    bucket_name = settings.S3_BUCKET_NAME

    s3_setup = S3PublicAccessSetup(bucket_name)

    logger.info(f"バケット {bucket_name} の公開設定を開始します。")
    s3_setup.enable_public_access()
    s3_setup.set_public_read_policy()
    logger.info(f"バケット {bucket_name} の公開設定が完了しました。")
