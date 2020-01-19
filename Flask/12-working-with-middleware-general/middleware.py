from werkzeug.wrappers import Request, Response


class Middleware():
    def __init__(self, app):
        self.app = app
        self.username = 'TestUser'
        self.password = 'TestPass'

    def __call__(self, environ, start_response):
        request = Request(environ)
        username = request.authorization['username']
        password = request.authorization['password']

        if username == self.username and password == self.password:
            environ['user'] = {
                'name': 'Test User'
            }

            return self.app(environ, start_response)

        res = Response('Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)