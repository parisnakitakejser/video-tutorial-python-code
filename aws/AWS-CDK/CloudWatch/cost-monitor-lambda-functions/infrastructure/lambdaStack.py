from aws_cdk import (
    Duration,
    NestedStack,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as events_targets,
)
from constructs import Construct


class LambdaStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.func_test = lambda_.Function(
            self,
            "testLambda",
            code=lambda_.Code.from_asset("assets/lambda/testLambda"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            log_retention=logs.RetentionDays.ONE_WEEK,
            timeout=Duration.minutes(15),
            memory_size=512,
        )

        self.func_monitor = lambda_.Function(
            self,
            "monitorLambda",
            code=lambda_.Code.from_asset("assets/lambda/monitorMetrics"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        self.func_monitor.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "cloudwatch:*",
                    "lambda:GetFunctionConfiguration",
                ],
                resources=["*"],
            )
        )

        events.Rule(
            self,
            "ScheduleRule",
            schedule=events.Schedule.cron(minute="*/5"),
            targets=[events_targets.LambdaFunction(self.func_monitor)],
        )
