from aws_cdk import Stack, aws_elasticloadbalancingv2 as elbv2, aws_ec2 as ec2
from constructs import Construct

from infrastructure.loadbalancePublicStack import LoadbalancePublicStack

from infrastructure.networkStack import NetworkStack


class PrototypeALBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.network = NetworkStack(self, "NetworkStack")

        self.lb_public = elbv2.ApplicationLoadBalancer(
            self,
            "LB",
            load_balancer_name="lb-public",
            vpc=self.network.vpc_nat,
            internet_facing=True,
        )
        self.lb_public_listener = self.lb_public.add_listener(
            "PublicListener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200,
                message_body="This is a fixed response from ALB - NAT Public",
            ),
        )

        self.lb_private_one = elbv2.ApplicationLoadBalancer(
            self,
            "LBPrivateOne",
            load_balancer_name="lb-private-one",
            vpc=self.network.vpc_private_lb1,
        )

        self.lb_private_one_listener = self.lb_private_one.add_listener(
            "Listener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200, message_body="This is a fixed response from ALB - One"
            ),
        )

        self.lb_private_two = elbv2.ApplicationLoadBalancer(
            self,
            "LBPrivateTwo",
            load_balancer_name="lb-private-two",
            vpc=self.network.vpc_private_lb2,
        )

        self.lb_private_two_listener = self.lb_private_two.add_listener(
            "Listener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200, message_body="This is a fixed response from ALB - Two"
            ),
        )

        self.lb_public_stack = LoadbalancePublicStack(
            self,
            "LoadbalancePublicStack",
            vpc=self.network.vpc_nat,
            listener=self.lb_public_listener,
            lb_private_one_lb=self.lb_private_one,
            lb_private_two_lb=self.lb_private_two,
        )

        self.lb_public_stack.service.connections.allow_to(
            self.lb_private_one.connections, port_range=ec2.Port.tcp(80)
        )
