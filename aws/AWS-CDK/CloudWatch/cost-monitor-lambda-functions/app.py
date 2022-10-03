from aws_cdk import App
from infrastructure.prototypeCostStack import PrototypeCostStack


app = App()

PrototypeCostStack(app, "PrototypeCostStack")

app.synth()
