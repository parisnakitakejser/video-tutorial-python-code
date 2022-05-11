from aws_cdk import Stack
from constructs import Construct

from awsStack.apiGatewayStack import ApiGatewayStack


class awsRootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api_gateway = ApiGatewayStack(self, "ApiGatewayStack")
