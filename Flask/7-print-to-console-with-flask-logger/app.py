from flask import Flask, Response
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    print('Hello world - normal')
    print('Hello world - sys.stderr', file=sys.stderr)
    app.logger.info('Hello world - app.logger.info')

    return Response("test", status=200, mimetype='text/html')


app.run(port=5000)
