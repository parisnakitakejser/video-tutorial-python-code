from aws_cdk import (
    Duration,
    NestedStack,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_iam as iam,
)
from constructs import Construct


class LambdaStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.sns_topic = sns.Topic(self, "LambdaIvocationsLimitTopic")

        self.func_test = lambda_.Function(
            self,
            "testLambda",
            code=lambda_.Code.from_asset("assets/lambda/testLambda"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            log_retention=logs.RetentionDays.ONE_WEEK,
            timeout=Duration.minutes(15),
            memory_size=128,
        )

        self.func_test_alarm = cloudwatch.Alarm(
            self,
            "LambdaTestAlarm",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            threshold=5,
            evaluation_periods=30,
            datapoints_to_alarm=5,
            metric=self.func_test.metric_invocations(
                period=Duration.minutes(1),
            ),
        )

        self.func_test_alarm.add_alarm_action(
            cloudwatch_actions.SnsAction(self.sns_topic),
        )

        self.func_disable_heavy = lambda_.Function(
            self,
            "disableHeavyLambda",
            code=lambda_.Code.from_asset("assets/lambda/disableHeavyLambda"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            log_retention=logs.RetentionDays.ONE_WEEK,
        )
        self.func_disable_heavy.add_to_role_policy(
            iam.PolicyStatement(
                actions=["lambda:PutFunctionConcurrency"], resources=["*"]
            )
        )

        self.sns_topic.add_subscription(
            sns_subscriptions.LambdaSubscription(self.func_disable_heavy)
        )
