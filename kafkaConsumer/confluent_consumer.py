import time
import logging
import asyncio
import socket
from confluent_kafka import Consumer

import env
from helpers.event_processor import process_event

logger = logging.getLogger(__name__)

class KafkaConsumer(object):

    def __init__(self, bootstrap_server, consumer_topic) -> None:
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

    def _log_assignment(self, consumer, partitions) -> None:
        """log assingment policy."""
        logger.info("Consumer Assignments: {}".format(partitions))

    async def consume(self) -> None:
        """Consumer method that polls data from a topic."""
        logger.info("Kafka Consumer initialized to Consume for topics {}!".format(self.topics))
        self.consumer = Consumer(**self.consumer_config)
        self.consumer.subscribe(topics=self.topics, on_assign=self._log_assignment)
        start_time = time.time()
        while True:
            await asyncio.sleep(10)
            raw_message = self.consumer.poll()
            logger.info(f"Msg received from topic {raw_message.topic()} at offset :: {raw_message.offset()} at {start_time}")
            logger.info(f"msg :: {raw_message.value().decode('utf-8')}, headers :: {raw_message.headers()}")
            await process_event(
                raw_msg=raw_message.value(),
                logger=logger)
            self.consumer.commit() 

    def stop_consuming(self) -> None:
        """
        Perform any other garbage collection here
        :return:
        """
        logger.info("Shutting down Consumer.")
        self.consumer.close()

    def list_topics(self) -> None:
        self.consumer = Consumer(**self.consumer_config)
        return self.consumer.list_topics()


async def start_event_consumer() -> None:
    """Consumer controler to start and stop kafa consumer."""
    consumer = KafkaConsumer(env.BOOTSTRAP_SERVER, env.COMSUMER_TOPIC)
    try:
        await consumer.consume()
    except asyncio.CancelledError as e:
        logger.info(e)
    finally:
        consumer.stop_consuming()
