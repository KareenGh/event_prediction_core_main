import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

# Retry connection to Kafka
while True:
    try:
        consumer = KafkaConsumer("mm-topic", bootstrap_servers="kafka:9092", auto_offset_reset="earliest")
        producer = KafkaProducer(bootstrap_servers="kafka:9092")
        print("Connected to Kafka! ESM is listening for model selections...", flush=True)
        break
    except NoBrokersAvailable:
        print("Kafka not available yet, retrying in 5 seconds...", flush=True)
        time.sleep(5)

for message in consumer:
    model_decision = message.value.decode('utf-8')
    print(f"Received from mm-topic: {model_decision}", flush=True)

    # Dummy ML prediction logic
    prediction = f"Predicted event for: {model_decision}"
    producer.send("esm-topic", prediction.encode('utf-8'))  # Sending to `esm-topic`
    print(f"Sent to esm-topic: {prediction}", flush=True)
