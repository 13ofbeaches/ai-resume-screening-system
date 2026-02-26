import boto3
import os
from urllib.parse import urlparse

s3 = boto3.client('s3')

def download_from_s3(s3_url, download_folder="downloads"):

    os.makedirs(download_folder, exist_ok=True)

    parsed = urlparse(s3_url)

    bucket_name = parsed.netloc.split('.')[0]
    object_key = parsed.path.lstrip('/')

    local_file_path = os.path.join(
        download_folder,
        os.path.basename(object_key)
    )

    s3.download_file(bucket_name, object_key, local_file_path)

    print("Downloaded to:", local_file_path)

    return local_file_path