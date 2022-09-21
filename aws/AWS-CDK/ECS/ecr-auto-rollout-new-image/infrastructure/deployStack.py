from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_events_targets as events_targets,
    aws_lambda as lambda_,
)
from constructs import Construct


class DeployStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.Vpc,
        repository: ecr.Repository,
        ecs_cluster: ecs.Cluster,
        ecs_service: ecs.FargateService,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_event = lambda_.Function(
            self,
            "DeployEvent",
            code=lambda_.Code.from_asset("assets/lambda/deployEvent"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            retry_attempts=1,
            memory_size=128,
            vpc=vpc,
            environment={
                "CLUSTER_NAME": ecs_cluster.cluster_name,
                "SERVICE_NAME": ecs_service.service_name,
            },
        )
        self.lambda_event.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ecs:UpdateService"],
                resources=["*"],
            )
        )

        repository.on_cloud_trail_image_pushed(
            "RepositoryEvent",
            image_tag="latest",
            target=events_targets.LambdaFunction(self.lambda_event),
        )
