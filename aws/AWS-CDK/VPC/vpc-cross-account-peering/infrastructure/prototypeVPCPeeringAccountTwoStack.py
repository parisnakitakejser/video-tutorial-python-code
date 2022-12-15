from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct

from settings import AWS_ACCOUNT_ONE_ID, AWS_ACCOUNT_ONE_REGION, AWS_ACCOUNT_ONE_VPC_CIDR, AWS_ACCOUNT_TWO_VPC_CIDR, AWS_ACCOUNT_ONE_VPC_ID

class PrototypeVPCPeeringAccountTwoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Network
        self.vpc = ec2.Vpc(
            self,
            "Network",
            cidr=AWS_ACCOUNT_TWO_VPC_CIDR,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="PublicSubnet",
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="PrivateSubnet",
                ),
            ],
            max_azs=2,
            nat_gateways=1,
        )

        # Peering connection
        self.vpc_peering = ec2.CfnVPCPeeringConnection(
            self,
            "VPCPeering",
            vpc_id=self.vpc.vpc_id,
            peer_vpc_id=AWS_ACCOUNT_ONE_VPC_ID,
            peer_owner_id=AWS_ACCOUNT_ONE_ID,
            peer_region=AWS_ACCOUNT_ONE_REGION,
            peer_role_arn=f'arn:aws:iam::{AWS_ACCOUNT_ONE_ID}:role/VpcPeeringRole',
        )

        route_id = 0
        for vpc_subnet in self.vpc.private_subnets:
            route_id += 1

            ec2.CfnRoute(
                self,
                f"PeeringRouteNumber{route_id}",
                destination_cidr_block=AWS_ACCOUNT_ONE_VPC_CIDR,
                route_table_id=vpc_subnet.route_table.route_table_id,
                vpc_peering_connection_id=self.vpc_peering.ref,
            )
