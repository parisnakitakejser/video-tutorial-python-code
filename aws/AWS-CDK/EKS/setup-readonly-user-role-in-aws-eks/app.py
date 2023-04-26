from aws_cdk import App, Environment
from infrastructure.kubernetesStack import KubernetesStack

app = App()

env = Environment()

rds_stack = KubernetesStack(app, "KubernetesStack", env=env)

app.synth()
