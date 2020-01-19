from flask import Flask, request
from middleware import Middleware

app = Flask('app')
app.wsgi_app = Middleware(app.wsgi_app)

@app.route('/', methods=['GET'])
def hello_world():
    user = request.environ['user']['name']

    return f'Hi {user}'

if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)