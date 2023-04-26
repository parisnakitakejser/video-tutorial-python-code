from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

from infrastructure.networkStack import NetworkStack


class KubernetesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.network = NetworkStack(self, "NetworkStack")

        masters_role = iam.Role(
            self,
            "eks-admin",
            role_name="aws-eks-admin",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal(service="eks.amazonaws.com"),
                iam.AnyPrincipal(),  # importent, else a SSO user can't assume
            ),
        )
        masters_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )
        readonly_role = iam.Role(
            self,
            "eks-readonly",
            role_name="aws-eks-readonly",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal(service="eks.amazonaws.com"),
                iam.AnyPrincipal(),  # importent, else a SSO user can't assume
            ),
        )
        readonly_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        cluster = eks.Cluster(
            self,
            "aws-eks",
            version=eks.KubernetesVersion.V1_25,
            masters_role=masters_role,
            cluster_name="aws-eks-cluster",
            default_capacity=0,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.SCHEDULER,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
            ],
            vpc=self.network.vpc,
        )

        masters_role.grant_assume_role(cluster.admin_role)

        cluster.aws_auth.add_role_mapping(
            readonly_role, groups=["system:authenticated"]
        )

        self.__add_nodegroup(cluster=cluster)
        self.__add_addon(cluster=cluster)
        self.__add_readonly_member(
            cluster=cluster, readonly_role_arn=readonly_role.role_arn
        )

    def __add_nodegroup(self, cluster: eks.Cluster):
        instance_type_name = "m6i.large"

        self.nodegroup = eks.Nodegroup(
            self,
            "all-ng",
            cluster=cluster,
            nodegroup_name="primary-node-group",
            instance_types=[ec2.InstanceType(instance_type_name)],
            min_size=3,
            max_size=10,
            disk_size=100,
            labels={
                "instance-type": instance_type_name,
            },
        )

    def __add_addon(self, cluster: eks.Cluster):
        eks.CfnAddon(
            self,
            "vpc-cni-addon",
            addon_name="vpc-cni",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "coredns-addon",
            addon_name="coredns",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "kube-proxy-addon",
            addon_name="kube-proxy",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "aws-ebs-csi-driver-addon",
            addon_name="aws-ebs-csi-driver",
            cluster_name=cluster.cluster_name,
        )

    def __add_readonly_member(self, cluster: eks.Cluster, readonly_role_arn: str):
        cluster.add_manifest(
            "cluster-role",
            {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRole",
                "metadata": {
                    "name": "eks-access-cluster-role",
                    "namespace": "kube-system",
                },
                "rules": [
                    {
                        "apiGroups": [""],
                        "resources": [
                            "configmaps",
                            "services",
                            "pods",
                            "persistentvolumes",
                            "namespaces",
                        ],
                        "verbs": ["get", "list", "watch"],
                    },
                    {
                        "apiGroups": [""],
                        "resources": ["pods/log"],
                        "verbs": ["get", "list"],
                    },
                    {
                        "apiGroups": [""],
                        "resources": ["pods/portforward", "services/portforward"],
                        "verbs": ["create"],
                    },
                ],
            },
        )

        cluster.add_manifest(
            "cluster-role-binding",
            {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRoleBinding",
                "metadata": {
                    "name": "iam-cluster-role-binding",
                    "namespace": "kube-system",
                },
                "roleRef": {
                    "apiGroup": "rbac.authorization.k8s.io",
                    "kind": "ClusterRole",
                    "name": "eks-access-cluster-role",
                },
                "subjects": [
                    {
                        "kind": "User",
                        "name": readonly_role_arn,
                        "apiGroup": "rbac.authorization.k8s.io",
                    }
                ],
            },
        )
