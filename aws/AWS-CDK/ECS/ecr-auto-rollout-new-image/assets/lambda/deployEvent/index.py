import boto3
import os

client = boto3.client("ecs")

CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
SERVICE_NAME = os.environ.get("SERVICE_NAME")


def handler(event, _):
    print(event)

    response = client.update_service(
        cluster=CLUSTER_NAME, service=SERVICE_NAME, forceNewDeployment=True
    )

    print(response)
