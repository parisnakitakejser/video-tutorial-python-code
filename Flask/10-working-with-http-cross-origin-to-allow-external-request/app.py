from flask import Flask, Response
from json import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})


@app.route('/', methods=['GET'])
def home_page():
    return Response(dumps({
        'content': 'Hello world'
    }), mimetype='text/json')


app.run(port=5000)
