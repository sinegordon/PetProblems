import json

from multiprocessing import Queue
from typing import Dict, Any

from worker import WorkerHandle


class WorkerPool:
    def __init__(self, config: Dict[Any, Any]):
        self.queue = Queue()
        self.workers = []
        self.config = config
        count = self.config.get('workers', 2)
        self.add_worker(count)

    def add_worker(self, count):
        for _ in range(count):
            w = WorkerHandle(self.config, self.queue)
            self.workers.append(w)
            w.start()
        return 'Worker(s) added!'

    def del_worker(self, count):
        if count > len(self.workers) - 1:
            return 'Count lives workers must be positive!'
        for _ in range(count):
            w = self.workers.pop()
            w.kill()
        return 'Worker(s) deleted!'

    def get_processors_list(self):
        '''Not implemented'''
        return ''
    
    def get_transaction_result(self, transaction):
        if 'id' not in transaction:
            return json.dumps({'error': 'Unknown transaction ID'})
        for worker in self.workers:
            for res_id in worker.results:
                if transaction['id'] == res_id:
                    res = worker.results[res_id].copy()
                    del worker.results[res_id]
                    return json.dumps(res)
        return json.dumps({'error': 'Transaction ID not found in results'})

    def add_processor(self, name):
        message = {'method': 'add_processor', 'name': name}
        s = json.dumps(message)
        for worker in self.workers:
            worker.service_queue.put(s)
        return s

    def del_processor(self, name):
        message = {'method': 'del_processor', 'name': name}
        s = json.dumps(message)
        for worker in self.workers:
            worker.service_queue.put(s)
        return s

    def add_transaction(self, transaction):
        message = {'method': 'process_transaction', 'transaction': transaction}
        s = json.dumps(message)
        self.queue.put(s)
        return s
