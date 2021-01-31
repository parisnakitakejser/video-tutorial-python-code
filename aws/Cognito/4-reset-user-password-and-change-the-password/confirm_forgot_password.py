import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'hi@pnk.sh'
confirm_code = '580757'
password = '#Qwe1234'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
response = client.confirm_forgot_password(
    ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
    Username=username,
    ConfirmationCode=confirm_code,
    Password=password
)

print(response)