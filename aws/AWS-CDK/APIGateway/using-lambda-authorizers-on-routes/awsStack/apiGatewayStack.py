from constructs import Construct
from aws_cdk import NestedStack, aws_apigatewayv2_alpha as apigwv2_alpha
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from awsStack.lambdaStack import LambdaStack


class ApiGatewayStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_stack = LambdaStack(self, "LambdaStack")

        http_api = apigwv2_alpha.HttpApi(self, "APIGateway")

        http_api.add_routes(
            path="/user",
            methods=[apigwv2_alpha.HttpMethod.GET],
            integration=HttpLambdaIntegration(
                "ViewUser", self.lambda_stack.lambda_get_item
            ),
            authorizer=self.lambda_stack.lambda_authorizer,
        )
