import boto3
import datetime
import logging

from resources import calculate_time_range, put_cw_metric_data
from resources.lambda_ import ResourcesLambda

logging.basicConfig(level=logging.INFO)

lambdaclient = boto3.client("lambda", region_name="eu-central-1")


def handler(event, context):
    start, end = calculate_time_range()

    # for func in lambdaclient.list_functions()["Functions"]:
    for func in [{"FunctionArn": "{lambda-function-arn"}]:
        print("----")

        func_id = func["FunctionArn"].split(":")[-1]
        print("FunctionName:", func_id)

        lambda_exec = ResourcesLambda.calculate_exec(start=start, end=end, func=func_id)
        lambda_duration = ResourcesLambda.calculate_duration(
            start=start, end=end, func=func_id
        )
        lambda_memory = ResourcesLambda.get_memory(func=func_id)

        lambda_price_ms_pr_gb = 0.000016667 / 1000
        gb_used = lambda_memory / 1024
        execution_time = lambda_exec * lambda_duration

        price_cost = (execution_time * gb_used) * lambda_price_ms_pr_gb

        print(f"price_cost {price_cost}")

        put_cw_metric_data(
            count=price_cost,
            timestamp=datetime.datetime.utcnow(),
            arn=func["FunctionArn"],
        )


if __name__ == "__main__":
    handler(None, None)
