from aws_cdk import Stack
from constructs import Construct

from awsStack.lambdaStack import LambdaStack
from awsStack.networkStack import NetworkStack


class awsRootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.network_stack = NetworkStack(
            self,
            "NetworkStack",
        )

        self.lambda_stack = LambdaStack(
            self, "LambdaStack", network_stack=self.network_stack
        )
