import os
from dotenv import load_dotenv
from pymilvus import utility, connections

load_dotenv()

## connect to milvus
connections.connect(
    alias='default',
    host=os.getenv('MILVUS_HOST'), 
    port=os.getenv('MILVUS_PORT'),
    user=os.getenv('MILVUS_USER'),
    password=os.getenv('MILVUS_PASS'),
)

users = utility.reset_password('user', 'old_password', 'new_password', using='default')

print(users)