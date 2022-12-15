
from aws_cdk import Stack, aws_ec2 as ec2, aws_iam as iam
from constructs import Construct

from infrastructure.prototypeVPCPeeringAccountOneStack import PrototypeVPCPeeringAccountOneStack

from settings import AWS_ACCOUNT_TWO_VPC_CIDR, AWS_ACCOUNT_TWO_PEERING_ID

class PrototypeVPCPeerOneWithTwo(Stack):
    def __init__(self, scope: Construct, construct_id: str, network_one: PrototypeVPCPeeringAccountOneStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Peering connection
        route_id = 0
        for vpc_subnet in network_one.vpc.private_subnets:
            route_id += 1

            ec2.CfnRoute(
                self,
                f"PeeringRouteNumber{route_id}",
                destination_cidr_block=AWS_ACCOUNT_TWO_VPC_CIDR,
                route_table_id=vpc_subnet.route_table.route_table_id,
                vpc_peering_connection_id=AWS_ACCOUNT_TWO_PEERING_ID,
            )
