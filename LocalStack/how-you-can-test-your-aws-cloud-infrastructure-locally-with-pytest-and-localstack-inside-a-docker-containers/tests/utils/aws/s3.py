import boto3
import os

s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
)

s3_resource = boto3.resource(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
)


class MockS3:
    @staticmethod
    def createBucket(bucket_name: str):
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
            },
        )

    @staticmethod
    def garbageCollection(bucket_name: str):
        print(s3_client.list_buckets())

        s3_bucket = s3_resource.Bucket(bucket_name)
        bucket_versioning = s3_resource.BucketVersioning(bucket_name)

        if bucket_versioning.status == "Enabled":
            s3_bucket.object_versions.delete()
        else:
            s3_bucket.objects.all().delete()
