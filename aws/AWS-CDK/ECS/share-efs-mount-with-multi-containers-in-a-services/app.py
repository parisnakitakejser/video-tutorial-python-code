import aws_cdk

from infrastructure.sharedEFSMountInECSClusterPrototypeStack import (
    SharedEFSMountInECSClusterPrototypeStack,
)

app = aws_cdk.App()

SharedEFSMountInECSClusterPrototypeStack(
    app,
    "SharedEFSMountInECSClusterPrototypeStack",
)

app.synth()
