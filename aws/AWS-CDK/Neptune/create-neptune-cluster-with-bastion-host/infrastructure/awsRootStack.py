from aws_cdk import (
    Stack,
    Fn,
    CfnOutput,
    aws_neptune_alpha as neptune,
    aws_ec2 as ec2,
    aws_glue_alpha as glue,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_iam as iam,
)
from constructs import Construct


class awsRootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define VPC
        vpc = ec2.Vpc(self, "VPC")

        # Create Neptune Cluster
        neptune_sg = ec2.SecurityGroup(
            self,
            "NeptuneSecurityGroup",
            vpc=vpc,
            description="Security group for Neptune serverless cluster",
        )

        neptune_cluster = neptune.DatabaseCluster(
            self,
            "NeptuneServerless",
            vpc=vpc,
            security_groups=[neptune_sg],
            engine_version=neptune.EngineVersion.V1_2_0_0,
            instance_type=neptune.InstanceType.T4_G_MEDIUM,
        )
        neptune_cluster.connections.allow_default_port_from(neptune_sg)

        # Create Bastion host
        bastion_sg = ec2.SecurityGroup(
            self,
            "BastionSecurityGroup",
            vpc=vpc,
            description="Security group for bastion host",
        )

        bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH access")
        neptune_sg.add_ingress_rule(
            bastion_sg, ec2.Port.tcp(8182), "Neptune access from bastion host"
        )

        bastion_host = ec2.BastionHostLinux(
            self,
            "BastionHost",
            vpc=vpc,
            instance_name="BastionHost",
            security_group=bastion_sg,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # Create S3 Bucket and upload file
        s3_bucket = s3.Bucket(self, "glueFiles")
        s3_bucket_file = s3_deploy.BucketDeployment(
            self,
            "uploadFile",
            destination_bucket=s3_bucket,
            sources=[s3_deploy.Source.asset("neptune_python_utils.zip")],
            extract=False,
        )

        # Create Glue Job
        glue_role = iam.Role(
            self,
            "GlueRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSGlueServiceRole"
                ),
            ],
        )
        s3_bucket.grant_read(glue_role)

        glue_conn = glue.Connection(
            self,
            "MyConnection",
            type=glue.ConnectionType.NETWORK,
            # The security groups granting AWS Glue inbound access to the data source within the VPC
            security_groups=[neptune_sg],
            # The VPC subnet which contains the data source
            subnet=ec2.Subnet.from_subnet_attributes(
                self,
                "privatSubnet",
                subnet_id="subnet-0b655a2ba932eed0d",
                availability_zone="eu-west-2b",
            ),
        )

        glue_job = glue.Job(
            self,
            "PythonShellJob",
            job_name="glue-neptune-test-insert",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset("gremlin-insert.py"),
            ),
            description="an example Python Shell job",
            role=glue_role,
            connections=[glue_conn],
            default_arguments={
                "--extra-py-files": f"s3://{s3_bucket.bucket_name}/{Fn.select(0, s3_bucket_file.object_keys)}"
            },
        )

        neptune_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.all_traffic(), "Neptune access from Glue Job"
        )

        # # Print the command to connect to the Neptune cluster via the Bastion
        CfnOutput(
            self,
            "BastionKey",
            value=f"aws ec2-instance-connect send-ssh-public-key --instance-id {bastion_host.instance_id} --instance-os-user ec2-user --ssh-public-key file://~/.ssh/id_rsa.pub",
        )
        CfnOutput(
            self,
            "BastionProxy",
            value=f"ssh -i ~/.ssh/id_rsa -f -N -L 8182:{neptune_cluster.cluster_endpoint.hostname}:8182 ec2-user@{bastion_host.instance_public_dns_name} -v",
        )

        CfnOutput(
            self,
            "NeptuneStatus",
            value=f"curl http://{neptune_cluster.cluster_endpoint.hostname}/status",
        )
