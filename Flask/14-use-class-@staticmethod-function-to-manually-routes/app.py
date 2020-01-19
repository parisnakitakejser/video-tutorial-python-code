from flask import Flask
from helloWorld import HelloWorld

app = Flask('app')
app.add_url_rule('/', view_func=HelloWorld.test_route, methods=['GET'])

if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)