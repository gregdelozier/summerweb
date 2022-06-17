from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def get_index():
    return "<p>Hello from an extremely interesting web page!</p>"

@app.route("/hello")
def get_hello():
    return render_template('hello.html', name="Greg")

@app.route("/santa")
def get_santa():
    toy = request.args.get("toy","pony")
    return render_template('hello.html', name="Santa is sending a " + toy + "!")

@app.route("/hi")
@app.route("/hi/")
@app.route("/hi/<name>")
def get_hi(name="Dorothy"):
    return render_template('hello.html', name=name)

@app.route("/login", methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", "<missing name>")
    password = request.form.get("password", "<missing password>")
    if password == "password1":
        return redirect(url_for('get_hi', name=username))
    else:
        return redirect(url_for('get_login'))
