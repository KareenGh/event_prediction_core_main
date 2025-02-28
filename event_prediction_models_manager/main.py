import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer("ept-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! Models Manager is listening for logs...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    processed_log = message.value.decode('utf-8')
    print(f"Received from ept-topic: {processed_log}", flush=True)

    # Decide which model to use (dummy logic for now)
    model_decision = f"Using Model X for: {processed_log}"
    producer.send("mm-topic", model_decision.encode('utf-8'))  # ✅ Sending to `mm-topic`
    print(f"Sent to mm-topic: {model_decision}", flush=True)
