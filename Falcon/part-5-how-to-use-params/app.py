import json, falcon

class ObjRequstClass:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        validate_params = True
        
        if 'name' not in req.params:
            validate_params = False

        if 'age' not in req.params:
            validate_params = False


        if(validate_params is True):
            output = {
                'name' : req.params['name'],
                'age' : req.params['age'],
            }
        else:
            output = {
                'error' : 'You need name or age in your params'
            }

        resp.body = json.dumps(output)


api = falcon.API()
api.add_route('/params', ObjRequstClass())
