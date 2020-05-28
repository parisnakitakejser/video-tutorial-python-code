import json, falcon

class ObjRequstClass:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        data = json.loads(req.stream.read())

        output = {
            'msg' : 'Hello {0}'.format(data['name'])
        }
        resp.body = json.dumps(output)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        data = json.loads(req.stream.read())

        equel = int(data['x']) + int(data['y'])

        output = {
            'msg' : 'x: {x} + y: {y} is equel to {e}'.format(x=data['x'],y=data['y'],e=equel)
        }
        resp.body = json.dumps(output)

    def on_put(self, req, resp):
        resp.status = falcon.HTTP_200
        output = {
            'msg' : 'put is not supported for now - sorry :('
        }

        resp.body = json.dumps(output)

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_200
        output = {
            'msg' : 'delete is not supported for now - sorry :('
        }

        resp.body = json.dumps(output)



api = falcon.API()
api.add_route('/demo', ObjRequstClass())
