from aws_cdk import (
    Stack,
    Duration,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs as ecs,
    aws_ecr as ecr,
)
from constructs import Construct

from infrastructure.networkStack import NetworkStack
from infrastructure.ecsStack import EcsStack


class LBStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        lb_multi_domain_repository = ecr.Repository.from_repository_name(
            self,
            "RepositoryLBMultiDomains",
            repository_name="lb-multi-domains",
        )

        self.network = NetworkStack(self, "NetworkStack")

        self.lb = elbv2.ApplicationLoadBalancer(
            self,
            "LB",
            vpc=self.network.vpc,
            internet_facing=True,
            load_balancer_name="lb-multi-domain",
        )

        self.listener = self.lb.add_listener(
            f"HttpListener_{id}",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200, message_body="This is the ALB Default Action"
            ),
        )

        capacity = [
            # ecs.CapacityProviderStrategy(
            #     capacity_provider="FARGATE_SPOT", weight=75, base=0
            # ),
            ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE",
                weight=25,
                base=1,
            ),
        ]

        test_domain_1 = EcsStack(
            self,
            "test-domain1-ecs-stack",
            vpc=self.network.vpc,
            capacity=capacity,
            repository=lb_multi_domain_repository,
            listener=self.listener,
            domains=["example1.datatask-cloud.pnk.rest"],
            priority=10,
        )

        test_domain_2 = EcsStack(
            self,
            "test-domain2-ecs-stack",
            vpc=self.network.vpc,
            capacity=capacity,
            repository=lb_multi_domain_repository,
            listener=self.listener,
            domains=["example2.datatask-cloud.pnk.rest"],
            priority=20,
        )
