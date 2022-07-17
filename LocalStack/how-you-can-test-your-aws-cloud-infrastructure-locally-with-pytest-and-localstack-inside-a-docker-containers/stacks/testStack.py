from aws_cdk import Duration, Stack, aws_lambda as lambda_
from constructs import Construct

from os import path


class TestStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        root_path = path.dirname(path.abspath(__file__))

        self.test_layer = lambda_.LayerVersion(
            self,
            "TestLayer",
            code=lambda_.Code.from_asset(
                path.join(
                    root_path,
                    "lambda_layers/test_layer",
                ),
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
            license="Apache-2.0",
            description="A layer to test the L2 construct",
        )

        self.test_fn = lambda_.Function(
            self,
            "TestFunction",
            function_name="test-lambda-fn",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_handler.handler",
            layers=[self.test_layer],
            environment={},
            code=lambda_.Code.from_asset(
                path.join(
                    root_path,
                    "lambda_assets/test_fn",
                ),
            ),
        )
