from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct

from infrastructure.networkPeeringStack import NetworkPeeringStack


class NetworkStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Public - NAT
        self.vpc_nat = ec2.Vpc(
            self,
            "NetworkNAT",
            cidr="10.12.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="NATPublic",
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="NATPrivateSubnet_LB1",
                ),
            ],
            max_azs=2,
        )

        # Private - One
        self.vpc_private_lb1 = ec2.Vpc(
            self,
            "NetworkPrivateLb1",
            cidr="10.10.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="PrivateSubnet_LB1",
                )
            ],
            max_azs=2,
        )

        # Private - Two
        self.vpc_private_lb2 = ec2.Vpc(
            self,
            "NetworkPrivateLb2",
            cidr="10.11.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="PrivateSubnet_LB2",
                )
            ],
            max_azs=2,
        )

        # Peering Stack
        self.peering_stack = NetworkPeeringStack(
            self,
            "NetworkPeeringStack",
            nat_public=self.vpc_nat,
            vpc_one=self.vpc_private_lb1,
            vpc_two=self.vpc_private_lb2,
        )
