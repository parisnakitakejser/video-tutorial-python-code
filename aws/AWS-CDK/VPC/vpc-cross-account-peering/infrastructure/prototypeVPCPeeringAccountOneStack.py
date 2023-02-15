from aws_cdk import Stack, aws_ec2 as ec2, aws_iam as iam
from constructs import Construct

from settings import AWS_ACCOUNT_TWO_ID, AWS_ACCOUNT_ONE_VPC_CIDR

class PrototypeVPCPeeringAccountOneStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Network
        self.vpc = ec2.Vpc(
            self,
            "Network",
            cidr=AWS_ACCOUNT_ONE_VPC_CIDR,
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
            nat_gateways=1
        )

        # Peering role
        self.peering_role = iam.Role(self, "VpcPeeringRole", role_name='VpcPeeringRole', assumed_by=iam.AccountPrincipal(AWS_ACCOUNT_TWO_ID))
        self.peering_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "ec2:AcceptVpcPeeringConnection",
                "route53:CreateHostedZone",
                "route53:AssociateVPCWithHostedZone",
                "ec2:DescribeVpcs",
                "ec2:DescribeRegion",
            ],
            resources=["*"],
        ))
