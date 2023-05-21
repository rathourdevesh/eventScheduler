import time
import logging
import asyncio
import socket
from confluent_kafka import Consumer

import env

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class KafkaConsumer(object):

    def __init__(self, bootstrap_server, consumer_topic):
        """Init class for KafkaConsumer"""
        self.topics = consumer_topic
        self.consumer_config = {
            'bootstrap.servers': bootstrap_server,
            'group.id': env.CONSUMER_GROUP_ID,
            'default.topic.config': {
                'auto.offset.reset': 'latest'
            },
            'client.id': socket.gethostname(),
            'enable.auto.commit': False,
            'session.timeout.ms': 6000,
            'socket.keepalive.enable': True
        }

    def _log_assignment(self, consumer, partitions):
        """log assingment policy."""
        logger.info("Consumer Assignments: {}".format(partitions))

    async def consume(self):
        """Consumer method that polls data from a topic."""
        logger.info("Kafka Consumer Call to Consume for topics {}!".format(self.topics))
        self.consumer = Consumer(**self.consumer_config)
        self.consumer.subscribe(topics=self.topics, on_assign=self._log_assignment)
        start_time = time.time()
        while True:
            await asyncio.sleep(10)
            raw_message = self.consumer.poll()
            logger.info(f"Msg received from topic {raw_message.topic()} at offset :: {raw_message.offset()}")
            logger.info(f"{raw_message.value().decode('utf-8')} :: {raw_message.headers()}")
            print(f"{raw_message.value().decode('utf-8')} :: {raw_message.headers()}")
            self.consumer.commit() 

    def stop_consuming(self):
        """
        Perform any other garbage collection here
        :return:
        """
        logger.info("Shutting down Consumer.")
        self.consumer.close()

    def list_topics(self):
        self.consumer = Consumer(**self.consumer_config)
        return self.consumer.list_topics()


async def start_event_consumer():
    """Consumer controler to start and stop kafa consumer."""
    consumer = KafkaConsumer(env.BOOTSTRAP_SERVER, env.COMSUMER_TOPIC)
    try:
        await consumer.consume()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        consumer.stop_consuming()
