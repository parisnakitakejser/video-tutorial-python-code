import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'hi@pnk.sh'
confirm_code = '248659'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
response = client.confirm_sign_up(
    ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
    Username=username,
    ConfirmationCode=confirm_code
)

print(response)