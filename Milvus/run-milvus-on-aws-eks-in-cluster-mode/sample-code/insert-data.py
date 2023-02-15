import random
import os
from dotenv import load_dotenv
from pymilvus import Collection, connections

load_dotenv()

## connect to milvus
connections.connect(host=os.getenv('MILVUS_HOST'), port=os.getenv('MILVUS_PORT'))

# Parepare data
data = [
  [i for i in range(2000)],
  [i for i in range(10000, 12000)],
  [[random.random() for _ in range(2)] for _ in range(2000)],
]

# Get an existing collection.
collection = Collection("book")
mr = collection.insert(data)