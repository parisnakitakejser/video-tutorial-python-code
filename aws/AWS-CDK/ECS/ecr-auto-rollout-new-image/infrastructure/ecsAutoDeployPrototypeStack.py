from aws_cdk import Stack, aws_ecr as ecr
from constructs import Construct

from infrastructure.deployStack import DeployStack
from infrastructure.ecsStack import ECSStack
from infrastructure.networkStack import NetworkStack


class ECSAutoDeployPrototypeStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.repository = ecr.Repository.from_repository_name(
            self, "Repository", repository_name="ecs-deploy-prototype"
        )

        self.network = NetworkStack(self, "NetworkStack")
        self.ecs = ECSStack(
            self, "ECSStack", vpc=self.network.vpc, repository=self.repository
        )
        self.deploy = DeployStack(
            self,
            "DeployStack",
            vpc=self.network.vpc,
            repository=self.repository,
            ecs_cluster=self.ecs.cluster,
            ecs_service=self.ecs.service,
        )
