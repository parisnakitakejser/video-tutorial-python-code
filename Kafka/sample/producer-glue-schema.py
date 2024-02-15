import io
from avro.schema import parse
from avro.io import DatumWriter, BinaryEncoder
from kafka import KafkaProducer
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

schema = parse(schema_message['SchemaDefinition'])

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="PLAINTEXT",
)

message_object = {
    "name": "Evy Lina",
    "hotel": "Cheap Hotel",
    "dateFrom": "14-07-2024",
    "dateTo": "01-08-2021",
    "details": "Wish coffee ready"
}

# serialize the message data using the schema
buf = io.BytesIO()
encoder = BinaryEncoder(buf)
writer = DatumWriter(writers_schema=schema)
writer.write(message_object, encoder)
buf.seek(0)
message_data = (buf.read())

# Send the serialized message to the Kafka topic
producer.send(
    topic=TOPIC_NAME,
    value=message_data
)
producer.flush()
