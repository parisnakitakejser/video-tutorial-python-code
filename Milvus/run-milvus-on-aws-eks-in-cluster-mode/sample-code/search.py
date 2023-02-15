import os
from dotenv import load_dotenv
from pymilvus import Collection, connections

load_dotenv()

## connect to milvus
connections.connect(host=os.getenv('MILVUS_HOST'), port=os.getenv('MILVUS_PORT'))
# Get an existing collection.
collection = Collection("book")
# Vector search
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
  data=[[0.1, 0.2]],
  anns_field="book_intro", 
  param=search_params, 
  limit=10,
  expr=None
)

print(results)