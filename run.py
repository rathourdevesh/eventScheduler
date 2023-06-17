"""run consumer and workers in eventloop."""
import asyncio
import logging

import env
from kafkaConsumer.confluent_consumer import start_event_consumer
from worker.worker import start_worker

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()

try:
    if env.MODE == "consumer":
        task2 = asyncio.ensure_future(start_event_consumer())
        logger.info(f"Starting Consumer...")
        process2 = loop.run_until_complete(task2)
    elif env.MODE == "worker":
        task1 = asyncio.ensure_future(start_worker())
        logger.info(f"initializing Worker...")
        process1 = loop.run_until_complete(task1)
except KeyboardInterrupt as error:
    logger.info(error)
finally:
    loop = asyncio.get_event_loop()
    loop.stop()
    exit()
