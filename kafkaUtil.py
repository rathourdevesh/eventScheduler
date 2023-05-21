from kafka import KafkaProducer, KafkaConsumer
import time
import json

class Scheduler:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.tasks = []
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers,
                                      auto_offset_reset='latest',
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    
    def add_task(self, task, interval):
        self.tasks.append((task, interval))
        self.producer.send('tasks', {'task': task.__name__, 'interval': interval})
    
    def run(self):
        self.consumer.subscribe(['tasks'])
        while True:
            for message in self.consumer:
                task = next((t for t in self.tasks if t[0].__name__ == message.value['task']), None)
                if task:
                    if time.time() - task[1] > message.value['interval']:
                        task[0]()
                        task[1] = time.time()
            time.sleep(0.01)

def print_hello():
    print("Hello!")

scheduler = Scheduler()
scheduler.add_task(print_hello, 1)

scheduler.run()
