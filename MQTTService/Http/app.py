import falcon
import json
from bson import ObjectId


from worker import Worker

worker = Worker(json.load(open('./http_config.json')))

class MongoEngineEncoder(json.JSONEncoder):
    '''Simple encoder for MongoCollection'''
    def default(self, obj):

        if isinstance(obj, ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

class Test():
    '''Test API method'''
    def on_get(self, req, resp):
        try:
            data = worker.test({ 'timestamp': int(req.params['timestamp']) })
            resp.media = json.dumps(data, cls=MongoEngineEncoder)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            print('Response - 200')
        except Exception as ex:
            print(str(ex))
            resp.status = falcon.HTTP_500
            print('Response - 500')

    def on_post(self, req, resp):
        try:
            data = worker.test(req.media)
            resp.media = json.dumps(data, cls=MongoEngineEncoder)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            print('Response - 200')
        except Exception as ex:
            print(str(ex))
            resp.status = falcon.HTTP_500
            print('Response - 500')

# Run API
api = falcon.API()
api.req_options.auto_parse_form_urlencoded = True
test = Test()
api.add_route('/api/test', test)