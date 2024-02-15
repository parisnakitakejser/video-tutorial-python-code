from kafka import KafkaConsumer
import io
import avro.schema
import avro.io
import boto3

from settings import (
    BOOTSTRAP_SERVERS,
    GLUE_SCHEMA,
    GLUE_STREAM_SCHEMA_REGISTRY,
    TOPIC_NAME,
)

glue = boto3.client('glue')

schema_message = glue.get_schema_version(
    SchemaId={
        'SchemaName': GLUE_SCHEMA,
        'RegistryName': GLUE_STREAM_SCHEMA_REGISTRY
    },
    SchemaVersionNumber={
        'LatestVersion': True
    }
)

schema = avro.schema.parse(schema_message['SchemaDefinition'])

# To consume messages
consumer = KafkaConsumer(
    TOPIC_NAME,
    group_id='my_group',
    bootstrap_servers=BOOTSTRAP_SERVERS,
)

for msg in consumer:
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    booking = reader.read(decoder)
    print(booking)
