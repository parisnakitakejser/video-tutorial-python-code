from platform import architecture
from aws_cdk import (
    NestedStack,
    Duration,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elb2,
)
from constructs import Construct


class ECSStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.Vpc,
        repository: ecr.Repository,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.load_balancer = elb2.ApplicationLoadBalancer(
            self,
            "ServiceLB",
            http2_enabled=True,
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="ecs-deploy-service-lb",
        )

        self.cluster = ecs.Cluster(
            self,
            "Cluster",
            container_insights=True,
            vpc=vpc,
            enable_fargate_capacity_providers=True,
        )

        capacity = [
            ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE_SPOT", weight=75, base=0
            ),
            ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE",
                weight=25,
                base=1,
            ),
        ]

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

        self.listener = self.load_balancer.add_listener(
            "HttpListener",
            port=80,
            protocol=elb2.ApplicationProtocol.HTTP,
        )

        self.targets = self.listener.add_targets(
            "HttpTG",
            targets=[self.service],
            port=5000,
            protocol=elb2.ApplicationProtocol.HTTP,
            deregistration_delay=Duration.seconds(10),
            slow_start=Duration.seconds(30),
            health_check=elb2.HealthCheck(enabled=True, path="/health"),
        )
