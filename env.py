import os
import socket

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")
COMSUMER_TOPIC = [os.getenv("COMSUMER_TOPIC")]
CONSUMER_GROUP_ID = os.getenv("CONSUMER_GROUP_ID")
MONGO_HOST = os.getenv("MONGO_HOST")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
MODE = os.getenv("MODE")

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
    'service_name': 'producer_service',
    'producer_config': {
        'bootstrap.servers':  BOOTSTRAP_SERVER,
    }
}
