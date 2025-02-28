import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer("col-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! Ranking Model is listening for collected data...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    collected_data = message.value.decode('utf-8')
    print(f"Received from col-topic: {collected_data}", flush=True)

    # Rank & Prioritize (Dummy Logic)
    ranked_event = f"High Priority Event: {collected_data}"
    producer.send("rm-topic", ranked_event.encode('utf-8'))  # ✅ Sending to `rm-topic`
    print(f"Sent to rm-topic: {ranked_event}", flush=True)
