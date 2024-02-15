from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    security_protocol="PLAINTEXT",
    value_serializer=lambda v: json.dumps(v).encode('ascii')
)

producer.send(
 'hotel-booking-request',
 value={
     "name": "Evy Lina",
     "hotel": "Cheap Hotel",
     "dateFrom": "14-07-2024",
     "dateTo": "01-08-2021",
     "details": "Wish coffee ready 😀"
     }
)
producer.flush()
