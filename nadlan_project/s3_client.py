import boto3
import os
access_key = os.environ.get("S3_ACCESS_KEY")
# s3_client = boto3.client("s3", aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
#                          aws_secret_access_key=os.environ.get("S3_SECRET_KEY"))
#
# res = s3_client.list_buckets()
# buckets = res.get("Buckets")
# print(buckets)

print(access_key)
