from aws_cdk import App
from infrastructure.prototypeStack import PrototypeStack


app = App()

PrototypeStack(app, "PrototypeLambdaWithEFSAccessPoint")

app.synth()
