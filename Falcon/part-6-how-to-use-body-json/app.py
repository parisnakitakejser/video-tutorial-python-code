import json, falcon

class ObjRequstClass:
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        json_validate = False

        try:
            json_input = json.loads(req.stream.read())
            json_validate = True
        except:
            json_input = {}

        if json_validate is not True:
            resp.status = falcon.HTTP_404
            output = {
                'validate' : {
                    'status' : 404,
                    'msg' : 'json data not validated currect.'
                }
            }

        else:
            if 'name' not in json_input:
                output = {
                    'welcom_msg' : 'Hello guest, how are you?'
                }
            elif 'age' not in json_input:
                output = {
                    'welcom_msg' : 'Hello {name}, what is your age?'.format(name=json_input['name'])
                }
            else:
                output = {
                    'welcom_msg' : 'Hello {name}, you are {age} years old.'.format(name=json_input['name'],age=json_input['age'])
                }

        resp.body = json.dumps(output)


api = falcon.API()
api.add_route('/body-json', ObjRequstClass())
