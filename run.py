"""run consumer and workers in eventloop."""
import asyncio
import logging
from kafkaConsumer.confluent_consumer import start_event_consumer
# from worker import worker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loop = asyncio.get_event_loop()
# task1 = asyncio.ensure_future(worker())
task2 = asyncio.ensure_future(start_event_consumer())

try:
    # loop.run_until_complete(task1)
    process = loop.run_until_complete(task2)
except Exception as error:
    logger.error(error)
finally:
    loop.close()
