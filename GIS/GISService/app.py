import falcon
import json

from worker import Worker

worker = Worker(json.load(open('./service_config.json')))

class Test():
    '''Test API method'''
    def on_get(self, req, resp):
        try:
            resp.body = worker.test(json.loads(req.params['json']))
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
    def on_post(self, req, resp):
        try:
            resp.body = worker.test(req.media)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500

# Run API
api = falcon.API()
api.req_options.auto_parse_form_urlencoded = True
test = Test()
api.add_route('/api/test', test)