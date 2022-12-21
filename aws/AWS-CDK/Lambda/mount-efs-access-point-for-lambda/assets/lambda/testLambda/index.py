import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = os.getenv("BUCKET_NAME")
EFS_MOUNT = os.getenv("EFS_MOUNT")
TEMP_DIR = os.getenv("TEMP_DIR")


def handler(events, context):
    s3_file_path = "{your-s3-file-path}"
    local_temp_file = f"{TEMP_DIR}/file-name.zip"
    efs_file_path = f"{EFS_MOUNT}/custom-filename.zip"

    os.makedirs(TEMP_DIR, exist_ok=True)
    with open(local_temp_file, "wb") as f:
        s3.download_fileobj(BUCKET_NAME, s3_file_path, f)

    os.system(f"cp {local_temp_file} {efs_file_path}")

    print(os.system(f"ls -la {EFS_MOUNT}"))

    return {"statusCode": 200}
