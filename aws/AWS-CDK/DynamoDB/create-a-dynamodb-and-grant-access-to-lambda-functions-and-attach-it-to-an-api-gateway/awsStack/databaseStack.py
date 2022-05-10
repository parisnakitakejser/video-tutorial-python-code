from constructs import Construct
from aws_cdk import (
    NestedStack, aws_dynamodb as dynamodb
)


class DynamoDBStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.test_table = dynamodb.Table(self, "TestTable", table_name="TestTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
        )
