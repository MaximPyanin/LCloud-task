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

    def get_objects(self):
        response = self._client.list_objects_v2(
            Bucket=self.config.BUCKET_NAME, Prefix=self.config.DIRECTORY
        )
        if "Contents" in response:
            for item in response["Contents"]:
                print(item["Key"])
        else:
            print("No files found")
