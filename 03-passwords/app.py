from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, make_response
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.secret_key="ksmdflkji240[i2hjfsklnf"

@app.route("/")
@app.route("/home")
def get_index():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('get_login'))
    return render_template('home.html', name=username)

@app.route("/other")
def get_other():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('get_login'))
    return render_template('other.html', name=username)

@app.route("/register", methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def post_register():
    username = request.form.get("username", None)
    if username == None:
        return redirect(url_for('get_register'))
    for c in username.lower():
        if not(c.isalpha() or c.isdigit() or (c in '.-_')):
            print("illegal character in username")
            return redirect(url_for('get_register'))        
    password = request.form.get("password", None)
    if password == None:
        return redirect(url_for('get_register'))
    if len(password) < 8:
        print("password not long enough")
        return redirect(url_for('get_register'))
    repeated = request.form.get("repeated", None)
    if repeated == None:
        return redirect(url_for('get_register'))
    if repeated != password:
        print("repeated password does not match password")
        return redirect(url_for('get_register'))
    # we have a legitimate registration, it seems

    # TODO: Do we have a user with this name already? 
    try:
        with open(f"storage/{username}.json", "r") as f:
            creds = json.load(f)
            print("user already exists")
            return redirect(url_for('get_register'))
    except Exception as e:
        pass

    # TODO: store the user credentials
    creds = {
        "username":username,
        "password":generate_password_hash(password)
    }
    with open(f"storage/{username}.json","w") as f:
        json.dump(creds, f)

    # return the logged-in user to a session
    session['username'] = username
    return redirect(url_for('get_index'))

@app.route("/login", methods=['GET'])
def get_login():
    if 'username' in session:
        return redirect(url_for('get_index'))
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", None)
    if username == None:
        return redirect(url_for('get_login'))
    try:
        with open(f"storage/{username}.json", "r") as f:
            creds = json.load(f)
    except Exception as e:
        print(f"Error in reading credentials. {e}")
        return redirect(url_for('get_login'))
    password = request.form.get("password", None)
    if not check_password_hash(creds['password'], password):
        print(f"Error - bad password.")
        return redirect(url_for('get_login'))
    session['username'] = username
    return redirect(url_for('get_index'))

@app.route("/logout", methods=['GET'])
def get_logout():
    session.pop('username',None) 
    return redirect(url_for('get_login'))

