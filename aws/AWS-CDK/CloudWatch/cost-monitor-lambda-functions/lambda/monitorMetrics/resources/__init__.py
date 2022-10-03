import logging
import datetime
import boto3

METRIC_WINDOW = 5
METRIC_DELAY = 10

cwclient = boto3.client("cloudwatch", region_name="eu-central-1")


def calculate_time_range():
    start = datetime.datetime.utcnow() + datetime.timedelta(minutes=-METRIC_DELAY)
    end = start + datetime.timedelta(minutes=METRIC_WINDOW)

    logging.info(f"start:[{start}] - end:[{end}]")

    return start, end


def put_cw_metric_data(count, timestamp, arn):
    response = cwclient.put_metric_data(
        Namespace="ConcurrencyLabs/Pricing/NearRealTimeForecast",
        MetricData=[
            {
                "MetricName": "EstimatedCharges",
                "Dimensions": [
                    {"Name": "Currency", "Value": "USD"},
                    {"Name": "ServiceName", "Value": "lambda"},
                    {"Name": "ServiceArn", "Value": arn},
                ],
                "Timestamp": timestamp,
                "Value": count,
                "Unit": "Count",
            }
        ],
    )

    print(response)
