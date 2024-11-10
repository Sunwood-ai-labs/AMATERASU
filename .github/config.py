from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import os

class Settings(BaseSettings):
    # 既存の設定
    # LITELLM_MODEL: str = "gemini/gemini-1.5-flash-exp-0827"
    LITELLM_MODEL: str = "gemini/gemini-1.5-flash-002"
    GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")
    GITHUB_REPOSITORY: str = Field(..., env="GITHUB_REPOSITORY")
    ISSUE_NUMBER: int = Field(0, env="ISSUE_NUMBER")
    REPOSITORY_SUMMARY_PATH: str = Field("", env="REPOSITORY_SUMMARY_PATH")
    YOUR_PERSONAL_ACCESS_TOKEN: str = Field("", env="YOUR_PERSONAL_ACCESS_TOKEN")
    YOUR_PERSONAL_ACCESS_TOKEN_IRIS: str = Field("", env="YOUR_PERSONAL_ACCESS_TOKEN_IRIS")
    RELEASE_NOTES_DIR: str = Field(default=os.path.join(os.path.dirname(__file__), "release_notes"), env="RELEASE_NOTES_DIR")
    DOCS_DIR: str = Field(default="./docs", env="DOCS_DIR")

    # GitHub Actionsの環境変数を使用してリポジトリの可視性を取得
    GITHUB_REPOSITORY_VISIBILITY: str = Field(default="public", env="GITHUB_REPOSITORY_VISIBILITY")

    # AWS S3関連の設定（オプショナル）
    USE_S3: bool = Field(default=False, env="USE_S3")
    AWS_ACCESS_KEY_ID: str = Field(default="", env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(default="", env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="ap-northeast-1", env="AWS_REGION")
    S3_BUCKET_NAME: str = Field(default="github-release-assets", env="S3_BUCKET_NAME")

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    @property
    def is_private_repo(self):
        return self.GITHUB_REPOSITORY_VISIBILITY == "private"

    @property
    def should_use_s3(self):
        return self.is_private_repo and self.USE_S3 and all([
            self.AWS_ACCESS_KEY_ID,
            self.AWS_SECRET_ACCESS_KEY,
            self.S3_BUCKET_NAME
        ])

@lru_cache()
def get_settings():
    return Settings()
