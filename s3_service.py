import boto3
from config_service import AppConfig


class S3Service:
    def __init__(self, config: AppConfig):
        self.config = config
        self._client = boto3.client(
            "s3",
            aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        )
