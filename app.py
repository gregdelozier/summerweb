from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

app = Flask(__name__)

username = None

@app.route("/")
@app.route("/home")
def get_index():
    global username
    if username == None:
        return redirect(url_for('get_login'))
    return render_template('home.html', name=username)

@app.route("/other")
def get_other():
    global username
    if username == None:
        return redirect(url_for('get_login'))
    return render_template('other.html', name=username)

@app.route("/login", methods=['GET'])
def get_login():
    global username
    if username != None:
        return redirect(url_for('get_index'))
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    global username
    username = request.form.get("username", None)
    return redirect(url_for('get_index'))

@app.route("/logout", methods=['GET'])
def get_logout():
    global username
    username = None
    return redirect(url_for('get_login'))

