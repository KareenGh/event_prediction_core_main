import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka!", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

while True:
    log_message = "Log from LFR container"
    producer.send("lfr-topic", log_message.encode('utf-8'))  # Sending to `lfr-topic`
    print(f"Sent to lfr-topic: {log_message}", flush=True)
    time.sleep(5)
