import json
import uuid
from confluent_kafka import Producer


class ProducerKafka():
    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def calling_producer(self, payload):
        p = Producer({
            'bootstrap.servers': 'localhost:9092',
        })

        sender_kafka_payload = {
            'key': '11231511551',
            'value': payload
        }

        dumps_payload = json.dumps(sender_kafka_payload).encode()
        p.produce('build-person-python-receive', key='python-sender', value=dumps_payload, callback=self.delivery_report)
        p.flush()