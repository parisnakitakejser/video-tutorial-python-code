from flask import Flask, Response
import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    template = jinja_env.get_template('layout.html')
    template_var = {
        'title': 'Jinja test var with flask'
    }

    return Response(template.render(template_var), mimetype='text/html'), 200


app.run(port=5000)
