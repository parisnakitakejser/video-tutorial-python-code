from constructs import Construct
from aws_cdk import Duration, NestedStack, aws_lambda as lambda_
from aws_cdk.aws_apigatewayv2_authorizers_alpha import (
    HttpLambdaAuthorizer,
    HttpLambdaResponseType,
)


class LambdaStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_authorizer = HttpLambdaAuthorizer(
            "UserAuthorizer",
            lambda_.Function(
                self,
                "UserAuthorizer",
                runtime=lambda_.Runtime.PYTHON_3_9,
                code=lambda_.Code.from_asset("lambdaAssets/apiGateway"),
                handler="userAuthorizer.lambda_handler",
            ),
            response_types=[HttpLambdaResponseType.SIMPLE],
            results_cache_ttl=Duration.seconds(0),  # Defualt 5min (300seconds)
        )

        self.lambda_get_item = lambda_.Function(
            self,
            "GetUser",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambdaAssets/apiGateway"),
            handler="getUser.lambda_handler",
        )
