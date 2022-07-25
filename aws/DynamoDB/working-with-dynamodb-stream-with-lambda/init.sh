export AWS_DEFAULT_REGION=eu-central-1

export lambda_function_name="dynamodb-stream-lambda"
export dynamodb_table_name="test-table"
export role_name="lambda-execute-dynamodb-stream-role"
export policy_name="lambda-dynamodb-stream-policy"
export sqs_dlq_name="test-table-dlq"

# Create DynamoDB with Stream enabled
export dynamodb=$(aws dynamodb create-table \
    --attribute-definitions AttributeName=PK,AttributeType=S \
    --table-name $dynamodb_table_name \
    --key-schema AttributeName=PK,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES)

export dynamodb_stream=$(echo $dynamodb | jq -r ".TableDescription.LatestStreamArn")

# Crete execute role
export role=$(aws iam create-role \
    --role-name $role_name \
    --assume-role-policy-document file://role.json)
export role_arn=$(echo $role | jq -r ".Role.Arn")

export policy_arn=$(aws iam create-policy \
    --policy-name $policy_name \
    --policy-document file://policy.json | jq -r ".Policy.Arn")

aws iam attach-role-policy \
    --role-name $role_name \
    --policy-arn $policy_arn

# Zip and create Lambda function
zip -j lambda-dynamoDBStream.zip lambda_assets/dynamoDBStream/*
aws lambda create-function \
    --function-name $lambda_function_name \
    --role $role_arn \
    --runtime python3.9 \
    --package-type Zip \
    --handler lambda_handler.handler \
    --zip-file fileb://./lambda-dynamoDBStream.zip
rm lambda-dynamoDBStream.zip

# Event source mapping
export event_source_mapping=$(aws lambda create-event-source-mapping \
    --function-name $lambda_function_name \
    --batch-size 5 \
    --maximum-batching-window-in-seconds 5 \
    --starting-position LATEST \
    --event-source-arn $dynamodb_stream)
export event_source_mapping_uuid=$(echo $event_source_mapping | jq -r ".UUID")

# Create SQS DLQ
export sqs_dlq=$(aws sqs create-queue --queue-name $sqs_dlq_name)
export sqs_dlq_url=$(echo $sqs_dlq | jq -r ".QueueUrl")

# SQS get QueueArn
export sqs_dlq_arn=$(aws sqs get-queue-attributes \
    --queue-url $sqs_dlq_url \
    --attribute-names QueueArn | jq -r ".Attributes.QueueArn")

# Update the event source mapping with DLQ mapping
aws lambda update-event-source-mapping \
    --uuid $event_source_mapping_uuid \
    --maximum-retry-attempts 2 \
    --maximum-record-age-in-seconds 3600 \
    --destination-config "{\"OnFailure\": {\"Destination\": \"$(echo $sqs_dlq_arn)\"}}"

# To process multiple batches concurrently
aws lambda update-event-source-mapping \
    --uuid $event_source_mapping_uuid \
    --parallelization-factor 5