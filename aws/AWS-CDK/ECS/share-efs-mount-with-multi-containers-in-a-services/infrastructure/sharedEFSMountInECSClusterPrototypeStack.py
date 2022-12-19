from aws_cdk import Stack, aws_ecr as ecr
from constructs import Construct

from infrastructure.ecsStack import ECSStack
from infrastructure.networkStack import NetworkStack


class SharedEFSMountInECSClusterPrototypeStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.network = NetworkStack(self, "NetworkStack")

        self.ecs = ECSStack(self, "ECSStack", vpc=self.network.vpc)
