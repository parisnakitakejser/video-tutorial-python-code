from aws_cdk import App

from stacks.testStack import TestStack

app = App()
TestStack(app, "TestStack")
app.synth()
