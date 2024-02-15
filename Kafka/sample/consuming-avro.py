from kafka import KafkaConsumer
import io
import avro.schema
import avro.io

from settings import AVRO_SCHEMA_FILE, BOOTSTRAP_SERVERS, TOPIC_NAME

schema = avro.schema.parse(open(AVRO_SCHEMA_FILE).read())

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
