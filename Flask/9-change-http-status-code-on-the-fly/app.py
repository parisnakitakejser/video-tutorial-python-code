from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/auth', methods=['GET'])
def auth_page():
    status_code = int(request.args.get('status', 200))
    return Response("Auth - user not allow", mimetype='text/html'), status_code


@app.route('/', methods=['GET'])
def home_page():
    return Response("Hello world", mimetype='text/html'), 200


app.run(port=5000)
