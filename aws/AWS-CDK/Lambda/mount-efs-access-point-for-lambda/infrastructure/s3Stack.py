from aws_cdk import (
    NestedStack,
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct


class S3Stack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self, "PrototypeBucket", removal_policy=RemovalPolicy.DESTROY
        )
