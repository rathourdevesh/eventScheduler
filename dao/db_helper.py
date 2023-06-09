"""functions for db interaction."""

import asyncio
import pymongo
import time

import env
from kafkaProducer.confluent_producer import KafkaProducer

class Scheduler:
    def __init__(self, uri=f"mongodb://{env.MONGO_HOST}/", db_name=env.DB_NAME, collection_name=env.COLLECTION_NAME):
        """Initialize mongo db as per envs."""
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def add_task(self, payload):
        """Insert task into mongo db."""
        try:
            task = {
                "last_run": time.time()
            }
            task.update(payload)
            self.collection.insert_one(task)
        except Exception as e:
            print(e)
    
    async def run(self):
        while True:
            try:
                tasks = self.collection.find()
                for task in tasks:
                    if time.time() > task["last_run"] + task["interval"] and task["retry"] > 0:
                        print(f"running task {task}")
                        KafkaProducer().produce_event(task.get("topic"), task.get("payload"))
                        self.collection.update_one(
                            {"_id": task["_id"]},
                            {"$set": {
                                "last_run": time.time(),
                                "retry": task["retry"] - 1}
                            },
                        )
            except Exception as e:
                print(e)
            await asyncio.sleep(0.9)
