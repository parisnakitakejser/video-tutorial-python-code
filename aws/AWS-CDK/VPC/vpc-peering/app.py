from aws_cdk import App
from infrastructure.prototypeAlbStack import PrototypeALBStack


app = App()

PrototypeALBStack(app, "PrototypeALBStack")

app.synth()
