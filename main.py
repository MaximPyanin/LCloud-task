from argparse import ArgumentParser
import os
from dotenv import load_dotenv
from config_service import AppConfig
from s3_service import S3Service


def main():
    config = AppConfig(os.environ)
    s3_service = S3Service(config)
    parser = ArgumentParser(description="S3 CLI")

    parser.add_argument("--list", action="store_true", help="list all files")

    parser.add_argument(
        "--upload",
        nargs=2,
        metavar=("LOCAL_PATH", "REMOTE_KEY"),
        help="upload a local file",
    )

    parser.add_argument("--filter", metavar="PATTERN", help="list files with regex")

    parser.add_argument(
        "--delete", metavar="PATTERN", help="delete all files with regex"
    )

    args = parser.parse_args()

    if args.list:
        s3_service.get_objects()
    if args.upload:
        filepath, key = args.upload
        s3_service.upload_file(filepath, key)
    if args.filter:
        pattern = args.filter
        s3_service.get_filtered_objects(pattern)
    if args.delete:
        pattern = args.delete
        s3_service.delete_filtered_objects(pattern)


if __name__ == "__main__":
    load_dotenv()
    main()
