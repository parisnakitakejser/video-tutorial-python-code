import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'hi@pnk.sh'
password = '#Abc1234'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
response = client.initiate_auth(
    ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
    }
)

# print(response)

print('AccessToken', response['AuthenticationResult']['AccessToken'])
print('RefreshToken', response['AuthenticationResult']['RefreshToken'])