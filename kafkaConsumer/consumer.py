"""Event consumer and save data to mongo db."""
import logging
from kafka import  KafkaConsumer
import asyncio
import json
import env

from dao.db_helper import save_data_in_db

logger = logging.getLogger(__name__)

class eventConsumer:
    def __init__(self, bootstrap_servers, consumer_topic):
        self.tasks = []
        self._bootstrap_servers = bootstrap_servers
        self._consumer_topic = consumer_topic

    def _log_assignment(self, consumer, partitions):
        logger.info(f"Consumer assingment: consumer: {consumer}, partition: {partitions}")

    async def consume(self):
        self.consumer = KafkaConsumer(bootstrap_servers=self._bootstrap_servers,
                                      auto_offset_reset='earliest')
        self.consumer.subscribe(self._consumer_topic)

        while True:
            await asyncio.sleep(0)
            raw_message = self.consumer.poll()
            if raw_message.error():
                logger.error(f"Error consuming data {raw_message.error()}")
            await save_data_in_db(json.loads(raw_message.value()))
            self.consumer.commit()

async def start_event_consumer():
    consumer = eventConsumer(env.BOOTSTRAP_SERVER, env.COMSUMER_TOPIC)
    await consumer.consume()
