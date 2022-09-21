import aws_cdk

from infrastructure.ecsAutoDeployPrototypeStack import ECSAutoDeployPrototypeStack

app = aws_cdk.App()

datacue_stack = ECSAutoDeployPrototypeStack(
    app,
    "ECSAutoDeployPrototypeStack",
)

app.synth()
