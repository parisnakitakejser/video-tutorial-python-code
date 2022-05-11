from constructs import Construct
from aws_cdk import NestedStack, aws_lambda as lambda_

from awsStack.networkStack import NetworkStack


class LambdaStack(NestedStack):
    def __init__(
        self, scope: Construct, id: str, network_stack: NetworkStack, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_get_item = lambda_.Function(
            self,
            "HelloWorld",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambdaAssets/"),
            handler="helloWorld.lambda_handler",
            vpc=network_stack.vpc_network,
        )
