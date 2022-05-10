from aws_cdk import Stack
from constructs import Construct

from awsStack.apiGatewayStack import ApiGatewayStack
from awsStack.databaseStack import DynamoDBStack
from awsStack.iamPolicyStack import IAMPolicyStack


class awsRootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # GeneralStacks
        self.api_gateway = ApiGatewayStack(self, "ApiGatewayStack")
        self.database = DynamoDBStack(self, "DynamoDBStack")

        # Policy Stack
        self.iam_policy = IAMPolicyStack(
            self, "IAMPolicyStack", database=self.database, api_gateway=self.api_gateway
        )
