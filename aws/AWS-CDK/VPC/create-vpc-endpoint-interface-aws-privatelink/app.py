from aws_cdk import App
from awsStack.awsRootStack import awsRootStack


app = App()
awsRootStack(app, "InterfaceVpcEndpointStack")
app.synth()
