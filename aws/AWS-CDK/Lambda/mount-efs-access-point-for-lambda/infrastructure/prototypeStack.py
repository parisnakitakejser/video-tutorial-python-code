from aws_cdk import (
    Stack,
    Size,
    RemovalPolicy,
    Duration,
    aws_lambda as lambda_,
    aws_ec2 as ec2,
    aws_efs as efs,
)
from constructs import Construct

from infrastructure.networkStack import NetworkStack
from infrastructure.s3Stack import S3Stack


class PrototypeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network_stack = NetworkStack(self, "NetworkStack")
        s3_stack = S3Stack(self, "S3Stack")

        # EFS (Elastic File System)
        self.file_system = efs.FileSystem(
            self,
            "EfsFileSystemService",
            vpc=network_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            lifecycle_policy=efs.LifecyclePolicy.AFTER_1_DAY,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.efs_access_point = self.file_system.add_access_point(
            "EfsAccessPoint",
            create_acl=efs.Acl(owner_uid="0", owner_gid="0", permissions="777"),
            posix_user=efs.PosixUser(uid="0", gid="0"),
        )

        self.file_system.connections.allow_default_port_from_any_ipv4()

        # Lambda copy function
        efs_mount_path = "/mnt/efs-volume-ml-model"

        lambda_func = lambda_.Function(
            self,
            "LambdaCopyFiles",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_asset("assets/lambda/testLambda"),
            environment={
                "BUCKET_NAME": s3_stack.bucket.bucket_name,
                "EFS_MOUNT": efs_mount_path,
                "TEMP_DIR": "/tmp/download",
            },
            vpc=network_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            filesystem=lambda_.FileSystem.from_efs_access_point(
                ap=self.efs_access_point, mount_path=efs_mount_path
            ),
            timeout=Duration.minutes(15),
            memory_size=1769,
            ephemeral_storage_size=Size.gibibytes(10),
        )
        s3_stack.bucket.grant_read(lambda_func)
