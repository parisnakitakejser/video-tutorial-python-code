from flask import Flask, Response
import logging
from logging.handlers import SMTPHandler

mail_handler = SMTPHandler(
    mailhost=('127.0.0.1', 1025),
    fromaddr='server@flask-test.localhost',
    toaddrs=['admin@flask-test.localhost'],
    subject='System error - log'
)

mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s %(levelname)s in %(module)s: %(message)s]'
))

app = Flask(__name__)
app.logger.addHandler(mail_handler)


@app.route('/', methods=['GET'])
def home_page():
    app.logger.debug('Logging - debug')
    app.logger.info('Logging - info')
    app.logger.warning('Logging - warning')
    app.logger.error('Logging - error')

    return Response("test", status=200, mimetype='text/html')


app.run(port=5000)
