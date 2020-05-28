import json, falcon

class ObjRequstClass:
    __json_content = {}

    def __validate_json_input(self, req):
        try:
            self.__json_content = json.loads(req.stream.read())
            print 'json from client is validated! :)'
            return True

        except ValueError, e:
            self.__json_content = {}
            print 'json from client is not validted :('
            return False

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        validated = self.__validate_json_input(req)

        output = {
            'status' : 200,
            'msg' : None
        }

        if(validated == True):
            if 'name' in self.__json_content:
                output['msg'] =  'Hello {name}'.format(name=self.__json_content['name'])
            else:
                output['status'] = 404
                output['msg'] = 'json input need name params'

        else:
            output['status'] = 404
            output['msg'] = 'json input is not validated'

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
