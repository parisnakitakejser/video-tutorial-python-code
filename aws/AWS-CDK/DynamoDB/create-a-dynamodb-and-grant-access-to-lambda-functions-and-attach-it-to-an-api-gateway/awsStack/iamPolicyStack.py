from constructs import Construct
from aws_cdk import NestedStack
from awsStack.apiGatewayStack import ApiGatewayStack
from awsStack.databaseStack import DynamoDBStack


class IAMPolicyStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        database: DynamoDBStack,
        api_gateway: ApiGatewayStack,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB - TestTable - Read & Write
        database.test_table.grant_read_write_data(
            api_gateway.lambda_stack.lambda_insert_item
        )

        # DynamoDB - TestTable - Read only
        database.test_table.grant_read_data(
            api_gateway.lambda_stack.lambda_get_item
        )
