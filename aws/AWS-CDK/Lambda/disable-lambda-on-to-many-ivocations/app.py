from aws_cdk import App
from infrastructure.prototypeDisableLambdaStack import PrototypeDisableLambdaStack


app = App()

PrototypeDisableLambdaStack(app, "PrototypeDisableLambdaStack")

app.synth()
