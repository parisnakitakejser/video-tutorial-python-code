import io
from avro.schema import parse
from avro.io import DatumWriter, BinaryEncoder
from kafka import KafkaProducer

from settings import AVRO_SCHEMA_FILE, BOOTSTRAP_SERVERS, TOPIC_NAME

schema = parse(open(AVRO_SCHEMA_FILE).read())

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
