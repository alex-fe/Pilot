import os
import datetime

import boto3
from botocore.client import Config

from keys import BUCKET_NAME, S3_ACCESS_KEY_ID, S3_ACCESS_SECRET_KEY


class Uploader(object):

    def __init__(self, flight_id):
        self.flight_id = str(flight_id)
        self.folder = os.path.join(
            self.flight_id, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            '{}'
        )
        self.upload_count = 0

    def upload(self, path):
        data = open(path, 'rb')
        s3 = boto3.resource(
            's3',
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        folder = self.folder.format(os.path.basename(path))
        s3.Bucket(BUCKET_NAME).put_object(Key=folder, Body=data)
        self.upload_count += 1
