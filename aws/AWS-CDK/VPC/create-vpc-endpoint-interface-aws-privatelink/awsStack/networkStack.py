from constructs import Construct
from aws_cdk import NestedStack, aws_ec2 as ec2


class NetworkStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc_network = ec2.Vpc(self, "TestVPC", cidr="10.0.0.0/16")

        ec2.InterfaceVpcEndpoint(
            self,
            "VPC Endpoint - .ecr.api",
            vpc=self.vpc_network,
            service=ec2.InterfaceVpcEndpointService(
                "com.amazonaws.eu-central-1.ecr.api"
            ),
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPC Endpoint - .ecr.dkr",
            vpc=self.vpc_network,
            service=ec2.InterfaceVpcEndpointService(
                "com.amazonaws.eu-central-1.ecr.dkr"
            ),
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPC Endpoint - .s3",
            vpc=self.vpc_network,
            service=ec2.InterfaceVpcEndpointService("com.amazonaws.eu-central-1.s3"),
        )
