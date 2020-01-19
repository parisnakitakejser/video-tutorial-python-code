from flask import Flask, g
from middleware import hello_middleware

app = Flask('app')


@app.route('/', methods=['GET'])
@hello_middleware
def hello_world():
    return f'token: {g.token}'


@app.route('/hello', methods=['GET'])
def hello_world_2():
    return 'hello section not hit middleware!'


if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)
