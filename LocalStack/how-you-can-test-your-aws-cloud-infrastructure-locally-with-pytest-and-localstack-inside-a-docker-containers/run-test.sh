# Create test network
docker network create test-network

# Setup localstack into test-network
docker run -d -it \
    --network=test-network \
    --name localstack \
    -p 4566:4566 \
    -p 4510-4559:4510-4559 \
    -e LOCALSTACK_API_KEY={pro-licens-key} \
    -e AWS_DEFAULT_REGION=eu-central-1 \
    localstack/localstack
    
echo "Sleep 10 sec, to besure localstart is running..."
sleep 10

# Setup and deploy CF to localstack
npm install -g aws-cdk-local aws-cdk
cdklocal --version
cdklocal bootstrap aws://000000000000/eu-central-1
cdklocal deploy --all --require-approval never

export AWS_DEFAULT_REGION=eu-central-1
awslocal lambda list-functions

# Build docker test images
docker build -f .deployment/unittest/Dockerfile -t unittest .

# Run docker unittest image
docker run --rm --network=test-network unittest

# # Cleanup process
docker image rm unittest

docker stop localstack
docker rm localstack

docker network rm test-network