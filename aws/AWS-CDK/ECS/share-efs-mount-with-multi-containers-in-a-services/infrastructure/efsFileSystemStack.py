from aws_cdk import NestedStack, aws_ec2 as ec2, aws_efs as efs
from constructs import Construct


class EFSFileSystemStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.file_system = efs.FileSystem(
            self,
            "EfsFileSystem",
            vpc=vpc,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_7_DAYS,  # files are not transitioned to infrequent access (IA) storage by default
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
            out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS,
        )
