# Cluster connection
Kubernetes cluster init by AWS CDK

Connection to Kubernetes cluster using AWS CLI as administrator

```
aws eks update-kubeconfig --name {cluster-name} --region {region} --role-arn arn:aws:iam::{account-id}:role/aws-eks-admin
```

Connection to Kubernetes cluster using AWS CLI as readonly member

```
aws eks update-kubeconfig --name {cluster-name} --region {region} --role-arn arn:aws:iam::{account-id}:role/aws-eks-readonly
```