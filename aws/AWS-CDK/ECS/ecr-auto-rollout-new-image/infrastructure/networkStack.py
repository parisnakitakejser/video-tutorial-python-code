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
            cidr="11.1.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT, name="Private"
                ),
            ],
            max_azs=2,
            nat_gateways=2,
        )
