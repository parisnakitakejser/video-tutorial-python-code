from ast import alias
from aws_cdk import (
    Stack,
    Duration,
    aws_elasticloadbalancingv2 as elbv2,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)
from constructs import Construct

from infrastructure.networkStack import NetworkStack

CERT_ARN = "arn:aws:acm:eu-central-1:685514959324:certificate/b3d2fb59-21c4-457e-b596-61c0102778f2"
HOSTED_ZONE_ID = "Z02819403QYY7KM5AMZ00"
DOMAIN_ROOT_NAME = "datatask-cloud.pnk.rest"
DOMAIN_RECORD_NAME = "lb-test.datatask-cloud.pnk.rest"


class LBStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.network = NetworkStack(self, "NetworkStack")

        self.lb = elbv2.ApplicationLoadBalancer(
            self,
            "LB",
            vpc=self.network.vpc,
            internet_facing=True,
            load_balancer_name="lb-multi-domain",
        )
        self.lb.add_redirect()

        self.listener = self.lb.add_listener(
            "HttpsListener",
            protocol=elbv2.ApplicationProtocol.HTTPS,
            certificates=[
                acm.Certificate.from_certificate_arn(
                    self,
                    "cert",
                    certificate_arn=CERT_ARN,
                )
            ],
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200, message_body="This is the ALB Default Action"
            ),
        )

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "LBTestHostedZoneID",
            hosted_zone_id=HOSTED_ZONE_ID,
            zone_name=DOMAIN_ROOT_NAME,
        )

        lb_custom_domain_target = route53.ARecord(
            self,
            "ARecord",
            target=route53.RecordTarget.from_alias(
                route53_targets.LoadBalancerTarget(self.lb)
            ),
            zone=hosted_zone,
            record_name=DOMAIN_RECORD_NAME,
            ttl=Duration.minutes(1),
        )
