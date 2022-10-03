from botocore.exceptions import ClientError
import boto3
import logging

from resources import METRIC_WINDOW

lambdaclient = boto3.client("lambda", region_name="eu-central-1")
cwclient = boto3.client("cloudwatch", region_name="eu-central-1")


class ResourcesLambda:
    @staticmethod
    def calculate_exec(start, end, func):
        result = 0

        invocations = cwclient.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Invocations",
            Dimensions=[{"Name": "FunctionName", "Value": func}],
            StartTime=start,
            EndTime=end,
            Period=60 * METRIC_WINDOW,
            Statistics=["Sum"],
        )

        print("invocations =>", invocations)

        for datapoint in invocations["Datapoints"]:
            if "Sum" in datapoint:
                result = result + datapoint["Sum"]

        return result

    @staticmethod
    def calculate_duration(start, end, func):
        result = 0
        count = 0
        total = 0

        invocations = cwclient.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Duration",
            Dimensions=[{"Name": "FunctionName", "Value": func}],
            StartTime=start,
            EndTime=end,
            Period=60 * METRIC_WINDOW,
            Statistics=["Average"],
        )

        print("invocations =>", invocations)

        for datapoint in invocations["Datapoints"]:
            if "Average" in datapoint:
                count += 1
                total += datapoint["Average"]

        if count:
            result = total / count

        return result

    @staticmethod
    def get_memory(func):
        result = 0
        args = {}

        args = {"FunctionName": func}

        try:
            response = lambdaclient.get_function_configuration(**args)
            if "MemorySize" in response:
                result = response["MemorySize"]

        except ClientError as e:
            logging.error(f"{e}")

        return result
