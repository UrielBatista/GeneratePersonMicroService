from kafka import KafkaConsumer
from AccessWeb.access_fake_it_cc import BrowserAccess
from ProducerTopic.producer_kafka import ProducerKafka

def consume_messages():
    consumer = KafkaConsumer(
        'build-person-python',
        bootstrap_servers=['10.0.0.4:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='build-person-data',
        value_deserializer=lambda x: x.decode('utf-8'))

    try:
        for message in consumer:
            print(f"Topic: {message.topic} Partition: {message.partition} Offset: {message.offset} Key: {message.key} Value: {message.value}")
            
            browser_fake_it = BrowserAccess()
            person = browser_fake_it.access_method(message.value)
            
            producer_kafka = ProducerKafka()
            producer_kafka.calling_producer(person)

    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
