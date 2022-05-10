import boto3
import uuid


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TestTable")
    item_id = uuid.uuid4().hex
    table.put_item(Item={"id": item_id, "testCode": "Your test string here"})

    return {"content": "Item insert into DynamoDB", "id": item_id}
