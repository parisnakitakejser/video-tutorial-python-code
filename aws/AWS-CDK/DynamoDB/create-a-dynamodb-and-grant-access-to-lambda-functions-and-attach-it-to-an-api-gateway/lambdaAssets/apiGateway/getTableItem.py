import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TestTable")
    table_item = table.get_item(Key={"id": event.get('pathParameters').get('itemId')})

    return {"content": "Get Table Item", "item": table_item}
