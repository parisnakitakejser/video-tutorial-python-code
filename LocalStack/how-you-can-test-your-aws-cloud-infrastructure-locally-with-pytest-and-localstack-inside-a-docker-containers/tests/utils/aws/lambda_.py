import boto3
import os
from json import dumps

lambda_client = boto3.client(
    "lambda",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
)


class MockLambda:
    @staticmethod
    def invoke(function_name: str, payload: dict = {}):
        response = lambda_client.invoke(
            FunctionName=function_name,
            # InvocationType="Event" | "RequestResponse" | "DryRun",
            # LogType="None" | "Tail",
            # ClientContext="string",
            Payload=dumps(payload),
            # Qualifier="string",
        )

        return response
