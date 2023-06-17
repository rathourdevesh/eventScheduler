import logging
from confluent_kafka import Producer
import json

import env

logger = logging.getLogger(__name__)

class KafkaProducer(object):

    def __init__(self) -> None:
        """Init class for KafkaProducer"""
        env.KAFKA_PRODUCER_CONFIG_DEFAULT_VALUES.update(env.ASYNC_PRODUCER_CONFIG["producer_config"])
        self.producer_config =  env.KAFKA_PRODUCER_CONFIG_DEFAULT_VALUES
        self.producer = Producer(**self.producer_config)

    def delivery_report(self, err, msg):
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

    def produce_event(self, topic, payload) -> None:
        """Produce event wrapper"""
        self.producer.produce(topic, json.dumps(payload).encode("utf-8"),
            callback=self.delivery_report)
        self.producer.flush(10)
