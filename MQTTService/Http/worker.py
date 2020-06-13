import json
from pymongo import MongoClient
from typing import Dict, Any




class Worker:
    def __init__(self, config: Dict[Any, Any]):
        self.config = config
        self.client = MongoClient(config['host'], config['port'])
        self.db = self.client[config['db']]
        self.collection = self.db[config['collection']]

    def test(self, data):
        ret = {'data': []}
        try:
            print(f"Data - {data}")
            ts = data['timestamp']
            ret['data'] = list(self.collection.find( { "timestamp": { "$gt": ts } } ))
            print(ret)
        except Exception as ex:
            err = str(ex)
            print(err)
            ret = {"error": err}
        return ret
