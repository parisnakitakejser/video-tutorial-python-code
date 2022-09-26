from typing import List

from aws_cdk import (
    NestedStack,
    Duration,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct


class EcsStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.Vpc,
        capacity: List[ecs.CapacityProviderStrategy],
        repository: ecs.ContainerImage,
        listener: elbv2.ApplicationListener,
        domains: List[str],
        priority: int,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(
            self,
            "Cluster",
            container_insights=True,
            vpc=vpc,
            enable_fargate_capacity_providers=True,
        )

        task_def = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            cpu=256,
            memory_limit_mib=512,
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=ecs.CpuArchitecture.ARM64,
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
            ),
        )

        task_def.add_container(
            "Container",
            image=ecs.ContainerImage.from_ecr_repository(repository, tag="latest"),
            port_mappings=[ecs.PortMapping(container_port=5000, host_port=None)],
            environment={
                "STACK_NAME": id,
            },
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=id,
                log_retention=logs.RetentionDays.ONE_MONTH,
            ),
        )

        self.service = ecs.FargateService(
            self,
            "Service",
            task_definition=task_def,
            cluster=self.cluster,
            desired_count=None,
            max_healthy_percent=200,
            min_healthy_percent=50,
            health_check_grace_period=Duration.seconds(100),
            capacity_provider_strategies=capacity,
            enable_ecs_managed_tags=True,
        )

        self.targets = listener.add_targets(
            f"HttpTG_{id}",
            priority=priority,
            conditions=[
                elbv2.ListenerCondition.host_headers(domains),
            ],
            targets=[self.service],
            port=5000,
            protocol=elbv2.ApplicationProtocol.HTTP,
            deregistration_delay=Duration.seconds(10),
            slow_start=Duration.seconds(30),
            health_check=elbv2.HealthCheck(enabled=True, path="/health"),
        )
