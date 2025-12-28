"""
Kafka producer for streaming application logs.
Real Kafka (Docker). Python 3.11.
"""

import json
import time
from kafka import KafkaProducer

KAFKA_TOPIC = "logs"
BOOTSTRAP_SERVERS = ["localhost:9092"]

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send_log(service, level, message):
    payload = {
        "service": service,
        "level": level,
        "message": message,
        "timestamp": time.time()
    }
    producer.send(KAFKA_TOPIC, payload)
    producer.flush()

if __name__ == "__main__":
    while True:
        send_log("auth-service", "ERROR", "Database connection timeout")
        time.sleep(5)