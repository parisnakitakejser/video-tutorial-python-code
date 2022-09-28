from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct


class NetworkPeeringStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        nat_public: ec2.Vpc,
        vpc_one: ec2.Vpc,
        vpc_two: ec2.Vpc,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Peering connection
        self.lb1_vpc_peering = ec2.CfnVPCPeeringConnection(
            self,
            "NATPublicToLBOnePrivate",
            vpc_id=nat_public.vpc_id,
            peer_vpc_id=vpc_one.vpc_id,
        )

        ec2.CfnRoute(
            self,
            "RouteFromPrivateSubnetOfVPCNatToVPCPrivateOne",
            destination_cidr_block=nat_public.vpc_cidr_block,
            route_table_id=vpc_one.isolated_subnets[0].route_table.route_table_id,
            vpc_peering_connection_id=self.lb1_vpc_peering.ref,
        )

        ec2.CfnRoute(
            self,
            "RouteFromPrivateSubnetOfVPCPrivateOneToVPCNat",
            destination_cidr_block=vpc_one.vpc_cidr_block,
            route_table_id=nat_public.public_subnets[0].route_table.route_table_id,
            vpc_peering_connection_id=self.lb1_vpc_peering.ref,
        )
