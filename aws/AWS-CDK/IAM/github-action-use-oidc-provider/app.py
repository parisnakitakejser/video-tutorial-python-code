from aws_cdk import App
from infrastructure.prototypeOIDCProvider import PrototypeOIDCProvider


app = App()

PrototypeOIDCProvider(app, "PrototypeOIDCProvider")

app.synth()
