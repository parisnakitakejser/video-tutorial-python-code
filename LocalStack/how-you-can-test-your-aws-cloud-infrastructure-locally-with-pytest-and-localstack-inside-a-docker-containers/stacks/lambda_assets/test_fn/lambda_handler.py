from helloWorld import respHello


def handler(event, context):
    return {
        "status": "success",
        "response": respHello(name="test-unit"),
        "event": event,
    }
