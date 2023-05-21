# from kafka import KafkaProducer
# import time
# import json

# class Scheduler:
#     def __init__(self,):
#         self.tasks = []
#         self.bootstrap_servers = ""
#         self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
#         # self.consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers,
#         #                               auto_offset_reset='latest',
#         #                               value_deserializer=lambda m: json.loads(m.decode('utf-8')))
#     def add_task(self):
#         print("sending")
#         self.producer.send('mytopic', "{'task': '555', 'interval': 0}".encode('utf-8'))

# scheduler = Scheduler()
# scheduler.add_task()

#     # def run(self):
#     #     self.consumer.subscribe(['mytopic1'])
#     #     while True:
#     #         for message in self.consumer:
#     #             task = next((t for t in self.tasks if t[0].__name__ == message.value['task']), None)
#     #             if task:
#     #                 if time.time() - task[1] > message.value['interval']:
#     #                     task[0]()
#     #                     task[1] = time.time()
#     #         time.sleep(0.01)




# # scheduler.run()

def delivery_report(err, msg):
    """Delivery Report For The Producer.

    Called once for each message produced to indicate delivery
    result. Triggered by poll() or flush()

    Args:
        self (obj): KafkaProducer class object.
        err (obj): Producer class error object.
        msg (obj): object of producer.

    """
    if err is not None:
       print(err)
    else:
        print(msg)


from confluent_kafka import Producer
import socket
import os

KAFKA_PRODUCER_CONFIG_DEFAULT_VALUES = {
    'default.topic.config': {'acks': 'all'},
    'socket.timeout.ms': 60000,
    'enable.idempotence': True,
    'client.id': socket.gethostname(),
    'socket.keepalive.enable': True,
    'message.max.bytes': 5000000,
    'compression.codec': 'lz4',
    'security.protocol': 'PLAINTEXT'
}


ASYNC_PRODUCER_CONFIG = {
    'service_name': 'chronos',
    'producer_config': {
        'bootstrap.servers': os.environ.get(
            'KAFKA_BROKER_LIST', 'localhost:9092'),
    }
}
KAFKA_PRODUCER_CONFIG_DEFAULT_VALUES.update(ASYNC_PRODUCER_CONFIG["producer_config"])
producer_config =  KAFKA_PRODUCER_CONFIG_DEFAULT_VALUES

producer = Producer(**producer_config)

producer.produce("mytopic1", "test msg1".encode("utf-8"),
    callback=delivery_report)

producer.flush(10)
