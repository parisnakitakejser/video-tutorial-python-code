from aws_cdk import Stack
from constructs import Construct

from infrastructure.lambdaStack import LambdaStack


class PrototypeCostStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_stack = LambdaStack(self, "LambdaStack")
