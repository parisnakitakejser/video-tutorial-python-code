from aws_cdk import (
    Stack, Duration,
    aws_iam as iam,
)
from constructs import Construct

GITHUB_ORG = 'your-github-org'
GITHUB_REPO = 'your-github-repo'

class PrototypeOIDCProvider(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        self.oidc_provider = iam.OpenIdConnectProvider(
            self,
            "githubProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
        )

        self.iam_role = iam.Role(
            self,
            "secure-cloud-access",
            role_name="secure-cloud-access",
            description=f"Access for github.com",
            assumed_by=iam.WebIdentityPrincipal(
                identity_provider=self.oidc_provider.open_id_connect_provider_arn,
                conditions={
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": f"repo:{GITHUB_ORG}/{GITHUB_REPO}:*",
                    }
                },
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
            max_session_duration=Duration.hours(1),
        )