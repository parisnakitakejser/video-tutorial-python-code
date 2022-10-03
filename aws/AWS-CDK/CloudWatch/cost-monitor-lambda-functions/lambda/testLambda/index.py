from time import sleep


def handler(event, context):
    print("Hello world! - Sleep in 5 sec")
    sleep(5)
    print("Wake up from sleep")
