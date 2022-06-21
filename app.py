from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

app = Flask(__name__)

username = "stranger"

@app.route("/")
@app.route("/home")
def get_index():
    global username
    return render_template('home.html', name=username)

@app.route("/login", methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    global username
    username = request.form.get("username", "stranger")
    return redirect(url_for('get_index'))
