import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer("esm-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! LLM is listening for predictions...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    prediction = message.value.decode('utf-8')
    print(f"Received from esm-topic: {prediction}", flush=True)

    # AI Processing (Dummy Logic)
    ai_enhancement = f"AI-enhanced: {prediction}"
    producer.send("llm-topic", ai_enhancement.encode('utf-8'))  # ✅ Sending to `llm-topic`
    print(f"Sent to llm-topic: {ai_enhancement}", flush=True)
