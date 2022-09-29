import aws_cdk
from infrastructure.lbStack import LBStack

app = aws_cdk.App()

lb_stack = LBStack(
    app,
    "LBStack",
)

app.synth()
