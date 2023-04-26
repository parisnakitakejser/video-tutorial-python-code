from aws_cdk import App
from infrastructure.awsRootStack import awsRootStack


app = App()
awsRootStack(app, "TestRootStack")
app.synth()
