import boto3
from config_service import AppConfig
import re


class S3Service:
    def __init__(self, config: AppConfig):
        self.config = config
        self._client = boto3.client(
            "s3",
            aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        )

    def get_objects(self) -> None:
        response = self._client.list_objects_v2(
            Bucket=self.config.BUCKET_NAME, Prefix=self.config.DIRECTORY
        )
        if "Contents" in response:
            for item in response["Contents"]:
                print(item["Key"])
        else:
            print("No files found")

    def upload_file(self, filepath: str, key: str) -> None:
        try:
            self._client.upload_file(
                filepath, self.config.BUCKET_NAME, f"{self.config.DIRECTORY}/{key}"
            )
            print(f"file uploaded to {key}")
        except Exception as error:
            print(f"error {error}while uploading")

    def get_filtered_objects(self, pattern: str) -> None:
        files = [
            item["Key"][len(self.config.DIRECTORY) + 1 :]
            for item in self._client.list_objects_v2(
                Bucket=self.config.BUCKET_NAME, Prefix=self.config.DIRECTORY
            )["Contents"]
            if re.match(pattern, item["Key"][len(self.config.DIRECTORY) + 1 :])
        ]
        if files:
            print(files)
        else:
            print(f"no files found for {pattern} filter ")
