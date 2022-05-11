def lambda_handler(event, context):
    return {
        "isAuthorized": True,
        "context": {
            "userId": "TestId",
        },
    }
