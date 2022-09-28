from aws_cdk import (
    NestedStack,
    Duration,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct


class LoadbalancePublicStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        listener: elbv2.ApplicationListener,
        lb_private_one_lb: elbv2.ApplicationLoadBalancer,
        lb_private_two_lb: elbv2.ApplicationLoadBalancer,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster = ecs.Cluster(
            self,
            "FargateCluster",
            vpc=vpc,
            enable_fargate_capacity_providers=True,
            container_insights=True,
        )

        self.task_definition = ecs.TaskDefinition(
            self,
            "TD",
            memory_mib="512",
            cpu="256",
            compatibility=ecs.Compatibility.FARGATE,
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=ecs.CpuArchitecture.ARM64
            ),
        )

        self.container = self.task_definition.add_container(
            "ContainerPublicNAT",
            image=ecs.ContainerImage.from_docker_image_asset(
                ecr_assets.DockerImageAsset(
                    self, "DockerImage", directory="container/public_image"
                )
            ),
            memory_limit_mib=256,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="container-public-nat",
                log_retention=logs.RetentionDays.ONE_MONTH,
            ),
            environment={
                "LB_ONE_DNS_NAME": lb_private_one_lb.load_balancer_dns_name,
                "LB_TWO_DNS_NAME": lb_private_two_lb.load_balancer_dns_name,
            },
        )
        self.container.add_port_mappings(
            ecs.PortMapping(container_port=5000, host_port=None)
        )

        capacity_provider = [
            # ecs.CapacityProviderStrategy(
            #     capacity_provider="FARGATE_SPOT", weight=75, base=0
            # ),
            ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE", weight=25, base=1
            ),
        ]

        self.service = ecs.FargateService(
            self,
            "Service",
            task_definition=self.task_definition,
            cluster=self.cluster,
            desired_count=None,
            max_healthy_percent=200,
            min_healthy_percent=50,
            health_check_grace_period=Duration.seconds(100),
            capacity_provider_strategies=capacity_provider,
        )

        self.targets = listener.add_targets(
            "ApplicationFleet",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[self.service],
            health_check=elbv2.HealthCheck(enabled=True, path="/health_check"),
            deregistration_delay=Duration.seconds(10),
            slow_start=Duration.seconds(30),
        )
