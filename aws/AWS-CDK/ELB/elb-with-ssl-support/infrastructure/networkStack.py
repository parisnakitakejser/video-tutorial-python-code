from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct


class NetworkStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "ServiceNetwork",
            cidr="12.1.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="Private",
                    cidr_mask=20,
                ),
            ],
            max_azs=2,
            nat_gateways=1,
        )
