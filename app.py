from flask import Flask

app = Flask(__name__)

@app.route("/")
def get_index():
    return "<p>Hello from an extremely interesting web page!</p>"

@app.route("/hello")
def get_hello():
    return "<p>Hello and welcome to Flask!</p>"
