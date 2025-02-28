import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        consumer = KafkaConsumer("lfr-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! EPT is listening for logs...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    log_data = message.value.decode('utf-8')
    print(f"Received from lfr-topic: {log_data}", flush=True)

    # Process log and forward to `ept-topic`
    processed_log = f"Processed: {log_data}"
    producer.send("ept-topic", processed_log.encode('utf-8'))   # Sending to `ept-topic`
    print(f"Sent to ept-topic: {processed_log}", flush=True)
