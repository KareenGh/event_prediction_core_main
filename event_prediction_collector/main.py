import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer("llm-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! Collector is listening for AI-enhanced results...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    ai_result = message.value.decode('utf-8')
    print(f"Received from llm-topic: {ai_result}", flush=True)

    # Collect & Aggregate (Dummy Logic)
    final_data = f"Collected Data: {ai_result}"
    producer.send("col-topic", final_data.encode('utf-8'))  # ✅ Sending to `col-topic`
    print(f"Sent to col-topic: {final_data}", flush=True)
