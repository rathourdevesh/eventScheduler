"""functions for db interaction."""

import pymongo
import time

class Scheduler:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='mytasks', collection_name='tasks'):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def add_task(self, task, interval):
        task_doc = {
            'name': task.__name__,
            'interval': interval,
            'last_run': time.time()
        }
        self.collection.insert_one(task_doc)
    
    def run(self):
        while True:
            tasks = self.collection.find()
            for task in tasks:
                if time.time() - task['last_run'] > task['interval']:
                    getattr(self, task['name'])()
                    self.collection.update_one(
                        {'_id': task['_id']},
                        {'$set': {'last_run': time.time()}}
                    )
            time.sleep(0.01)