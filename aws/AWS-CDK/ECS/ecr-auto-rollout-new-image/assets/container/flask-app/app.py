from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
