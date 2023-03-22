import os
from dotenv import load_dotenv
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection, connections

load_dotenv()

## connect to milvus
connections.connect(host=os.getenv('MILVUS_HOST'), port=os.getenv('MILVUS_PORT'))

# Prepare Schema
book_id = FieldSchema(name="book_id", dtype=DataType.INT64, is_primary=True)
word_count = FieldSchema(name="word_count", dtype=DataType.INT64)
book_intro = FieldSchema(name="book_intro", dtype=DataType.FLOAT_VECTOR, dim=2)
schema = CollectionSchema(fields=[book_id, word_count, book_intro], description="Test book search")
collection_name = "book"

# Create a collection with the schema
collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2)

collection.create_index(field_name="book_intro", index_params={"metric_type":"L2", "index_type":"IVF_FLAT", "params":{"nlist":1024}})
collection.load(replica_number=1)