from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    bootstrap_servers='localhost:29092',
    security_protocol="PLAINTEXT",
    value_deserializer=lambda v: json.loads(v.decode('ascii')),
    # auto_offset_reset='earliest'
)

consumer.subscribe(topics='hotel-booking-request')

for message in consumer:
    print(f"{message.partition}:{message.offset} v={message.value}")
