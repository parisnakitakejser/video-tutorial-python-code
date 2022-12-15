from infrastructure.prototypeVPCPeeringAccountOneStack import PrototypeVPCPeeringAccountOneStack
from infrastructure.prototypeVPCPeeringAccountTwoStack import PrototypeVPCPeeringAccountTwoStack
from infrastructure.prototypeVPCPeerOneWithTwo import PrototypeVPCPeerOneWithTwo
from aws_cdk import App

app = App()

network_one = PrototypeVPCPeeringAccountOneStack(app, "PrototypeVPCPeeringAccountOneStack")
network_two = PrototypeVPCPeeringAccountTwoStack(app, "PrototypeVPCPeeringAccountTwoStack")
network_connection = PrototypeVPCPeerOneWithTwo(app, "PrototypeVPCPeerOneWithTwo", network_one=network_one)

app.synth()
