from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return f"<h1>ECS STACK: {os.getenv('STACK_NAME')}</h1>"


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
