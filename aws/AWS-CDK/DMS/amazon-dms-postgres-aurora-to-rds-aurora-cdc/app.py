from aws_cdk import (
    Stack,
    App,
    Environment,
    RemovalPolicy,
    CfnOutput,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_dms as dms,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct
from json import dumps


class PostgresAuroraToInstanceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC for the RDS instances
        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=1,
            cidr="15.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
            ],
        )


        # Define the security group for the Aurora cluster
        source_cluster_sg = ec2.SecurityGroup(self, "SourceClusterSG", vpc=vpc, description="Security group for Aurora cluster")
        source_cluster_sg.add_ingress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.tcp(5432), "Allow access from the VPC")

        # Define the security group for the RDS instance
        target_instance_sg = ec2.SecurityGroup(self, "TargetInstanceSG", vpc=vpc, description="Security group for RDS instance")
        target_instance_sg.add_ingress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.tcp(5432), "Allow access from the VPC")


        # Create a security group for the DMS replication instance
        dms_replication_security_group = ec2.SecurityGroup(
            self,
            "DMSReplicationSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="dms-replication-sg",
        )

        # Create a Secrets Manager secret to store the password for the Aurora cluster
        source_secret = secretsmanager.Secret(
            self,
            "SourceSecret",
            description="Secret for Aurora cluster password",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                exclude_punctuation=True,
                secret_string_template=dumps({"username": 'dbuser'}),
                generate_string_key="password",
            ),
        )

        # Create a Secrets Manager secret to store the password for the RDS instance
        target_secret = secretsmanager.Secret(
            self,
            "TargetSecret",
            description="Secret for RDS instance password",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                exclude_punctuation=True,
                secret_string_template=dumps({"username": 'dbuser'}),
                generate_string_key="password",
            ),
        )
# Create an Aurora PostgreSQL cluster as the source database
        source_cluster = rds.DatabaseCluster(self, "SourceCluster",
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_13_4),
            instance_props=rds.InstanceProps(
                vpc=vpc,
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
                security_groups=[source_cluster_sg],
                auto_minor_version_upgrade=True,
            ),
            credentials=rds.Credentials.from_secret(source_secret),
            removal_policy=RemovalPolicy.DESTROY,
        )

       

        # Create a security group for the target RDS instance
        target_instance_security_group = ec2.SecurityGroup(
            self,
            "TargetInstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="target-instance-sg",
        )

        # Create an RDS PostgreSQL instance with a read replica as the target database
        target_instance = rds.DatabaseInstance(self, "TargetInstance",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_13),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
            vpc=vpc,
            security_groups=[target_instance_sg],
            deletion_protection=False,
            auto_minor_version_upgrade=True,
            credentials=rds.Credentials.from_secret(target_secret),
            removal_policy=RemovalPolicy.DESTROY,
            )

        # Create an Amazon DMS replication instance
        dms_replication_instance = dms.CfnReplicationInstance(
            self,
            "DMSReplicationInstance",
            replication_instance_class="dms.t2.micro",
            replication_instance_identifier="dms-replication-instance",
            allocated_storage=50,
            engine_version="3.4.7",
            publicly_accessible=False,
            vpc_security_group_ids=[dms_replication_security_group.security_group_id]
        )

        # Define the source and target endpoints for DMS
        source_endpoint = dms.CfnEndpoint(
            self,
            "SourceEndpoint",
            endpoint_type="source",
            engine_name="aurora-postgresql",
            database_name=source_cluster.cluster_identifier,
            username=source_cluster.secret.secret_value_from_json(
                "username"
            ).to_string(),
            password=source_cluster.secret.secret_value_from_json(
                "password"
            ).to_string(),
            server_name=source_cluster.cluster_endpoint.hostname,
            port=5432,
        )

        target_endpoint = dms.CfnEndpoint(
            self,
            "TargetEndpoint",
            endpoint_type="target",
            engine_name="postgres",
            database_name=target_instance.instance_identifier,
            username=target_instance.secret.secret_value_from_json(
                "username"
            ).to_string(),
            password=target_instance.secret.secret_value_from_json(
                "password"
            ).to_string(),
            server_name=target_instance.db_instance_endpoint_address,
            port=5432,
        )

        # Create a DMS task to replicate data from the source to the target
        dms_task = dms.CfnReplicationTask(
            self,
            "ReplicationTask",
            table_mappings="""{
                "rules": [
                    {
                        "rule-type": "selection",
                        "rule-id": "1",
                        "rule-name": "1",
                        "object-locator": {
                            "schema-name": "%",
                            "table-name": "%"
                        },
                        "rule-action": "include"
                    }
                ]
            }""",
            source_endpoint_arn=source_endpoint.ref,
            target_endpoint_arn=target_endpoint.ref,
            replication_instance_arn=dms_replication_instance.ref,
            migration_type="full-load-and-cdc",
        )

        CfnOutput(self, "OutputSourceEndpoint", value=source_endpoint.ref)
        CfnOutput(self, "OutputTargetEndpoint", value=target_endpoint.ref)


app = App()

rds_stack = PostgresAuroraToInstanceStack(app, "PostgresAuroraToInstanceStack")

app.synth()
