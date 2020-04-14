import falcon
import json

from pool import WorkerPool

pool = WorkerPool(json.load(open('./config.json')))

class AddTransactionToQueue():
    '''API method for transaction data processing'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.add_transaction(json.loads(req.params['json']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.add_transaction(req.media)
            #pool.add_transaction(req.media)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class AddProcessor():
    '''API method for add processor on the fly'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.add_processor(json.loads(req.params['json']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.add_processor(req.media)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class DelProcessor():
    '''API method for delete processor on the fly'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.del_processor(json.loads(req.params['json']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.del_processor(req.media)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class AddWorker():
    '''API method for add pool(s) on the fly'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.add_worker(int(req.params['count']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.add_worker(int(req.params['count']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class DelWorker():
    '''API method for delete pool(s) on the fly'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.del_worker(int(req.params['count']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.del_worker(int(req.params['count']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class GetProcessorsList():
    '''API method for show current pools list'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.get_processors_list()
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.get_processors_list()
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

class GetTransactionResult():
    '''API method for show result transaction'''
    def on_get(self, req, resp):
        try:
            resp.body = pool.get_transaction_result(json.loads(req.params['json']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = pool.get_transaction_result(req.media)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

# Run API
api = falcon.API()
api.req_options.auto_parse_form_urlencoded = True
add_transaction_to_queue = AddTransactionToQueue()
add_processor = AddProcessor()
del_processor = DelProcessor()
add_worker = AddWorker()
del_worker = DelWorker()
get_processors_list = GetProcessorsList()
get_transaction_result = GetTransactionResult()
api.add_route('/api/add_transaction', add_transaction_to_queue)
api.add_route('/api/add_processor', add_processor)
api.add_route('/api/del_processor', del_processor)
api.add_route('/api/add_worker', add_worker)
api.add_route('/api/del_worker', del_worker)
api.add_route('/api/get_processors_list', get_processors_list)
api.add_route('/api/get_transaction_result', get_transaction_result)