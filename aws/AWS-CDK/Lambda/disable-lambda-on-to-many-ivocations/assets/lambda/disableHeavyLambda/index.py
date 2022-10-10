from json import loads
import boto3

lambda_client = boto3.client("lambda")


def handler(event, context):
    print("event", event)

    for record in event.get("Records"):
        message = loads(record.get("Sns", {}).get("Message", {}))

        if message.get("Trigger", {}).get("Namespace") == "AWS/Lambda":
            for dimension in message.get("Trigger", {}).get("Dimensions"):
                if dimension.get("name") == "FunctionName":
                    print("dimension =>", dimension)

                    lambda_client.put_function_concurrency(
                        FunctionName=dimension.get("value"),
                        ReservedConcurrentExecutions=0,
                    )
                    break

        else:
            print("Not triggered by Lambda")
