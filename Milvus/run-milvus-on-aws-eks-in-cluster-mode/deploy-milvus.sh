eksctl create cluster -f eks-cluster.yml
aws eks --region eu-west-1 update-kubeconfig --name eks-cluster
helm repo add milvus https://milvus-io.github.io/milvus-helm/
helm upgrade --install --set cluster.enabled=true --set externalS3.enabled=true --set externalS3.host='s3.eu-west-1.amazonaws.com' --set externalS3.port=80 --set externalS3.accessKey={access-key} --set externalS3.secretKey={secret-key} --set externalS3.bucketName=milvus-data-{region}-{account-id} --set minio.enabled=False --set service.type=LoadBalancer milvus milvus/milvus