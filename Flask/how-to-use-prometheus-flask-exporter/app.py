from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/simple')
def simple_get():
    return {
        'status': '200'
    }

app.run(host='0.0.0.0', port=5001)