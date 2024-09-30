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

    def filter_objects(self, pattern: str) -> list[str]:
        return [
            item["Key"][len(self.config.DIRECTORY) + 1 :]
            for item in self._client.list_objects_v2(
                Bucket=self.config.BUCKET_NAME, Prefix=self.config.DIRECTORY
            )["Contents"]
            if re.match(pattern, item["Key"][len(self.config.DIRECTORY) + 1 :])
        ]

    def get_filtered_objects(self, pattern: str) -> None:
        files = self.filter_objects(pattern)
        if files:
            print(files)
        else:
            print(f"no files found for {pattern} filter ")

    def delete_filtered_objects(self, pattern: str) -> None:
        matched_objects = self.filter_objects(pattern)
        if matched_objects:
            for object in matched_objects:
                try:
                    self._client.delete_object(
                        Bucket=self.config.BUCKET_NAME,
                        Key=f"{self.config.DIRECTORY}/{object}",
                    )
                    print(f"file {object} deleted")
                except Exception as error:
                    print(f"error occured while  deleting file {object}: {error}")
        else:
            print("no files found for the given pattern")
