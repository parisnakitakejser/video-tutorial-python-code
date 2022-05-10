from constructs import Construct
from aws_cdk import NestedStack, aws_s3 as s3, aws_lambda as lambda_


class LambdaStack(NestedStack):
    def __init__(
        self, scope: Construct, id: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_insert_item = lambda_.Function(
            self,
            "InsertTableItem",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambdaAssets/apiGateway"),
            handler="insertTableItem.lambda_handler",
        )

        self.lambda_get_item = lambda_.Function(
            self,
            "GetTableItem",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambdaAssets/apiGateway"),
            handler="getTableItem.lambda_handler",
        )
