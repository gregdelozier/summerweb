from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import requests

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")

openweathermap_api = "<use your API from openweathermap>"

lat = 41.15
lon = -81.36

openweathermap_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_api}"
print(openweathermap_url)

def temp_f(temp_k): 
    return temp_k * 9.0/5.0 - 459.67

app = Flask(__name__)

@app.route("/map")
def get_map():
    result = requests.get(openweathermap_url)
    data = result.json()
    temp = temp_f(data['main']['temp'])
    print("The temp in Kent is ", temp)
    if temp < 30:
        color = "blue"
    elif temp < 60: 
        color = "green"
    elif temp < 90: 
        color = "yellow"
    else:
        color = "red"
    return render_template('map.html', temp=int(temp), color=color)

@app.route("/")
def get_list():
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list

    the_list = list(shopping_list.find({}))

    print(the_list)

    return render_template('list.html',list=the_list)

@app.route("/add_item", methods=['GET'])
def get_add_item():
    return render_template('add_item.html')

@app.route("/add_item", methods=['POST'])
def post_add_item():
    desc = request.form.get("desc", "<missing desc>")
    print("adding ",desc)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    shopping_list.insert_one({'desc':desc})

    return redirect(url_for('get_list'))

@app.route("/delete_item/<id>", methods=['GET'])
def get_delete_item(id):
    print("deleting id=",id)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    shopping_list.delete_one({'_id':id})

    return redirect(url_for('get_list'))

@app.route("/update_item/<id>", methods=['GET'])
def get_update_item(id):
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    the_item = shopping_list.find_one({"_id":id})
    return render_template('update_item.html',item=the_item)

from bson.objectid import ObjectId

@app.route("/update_item", methods=['POST'])
def post_update_item():
    _id = request.form.get("_id", "<missing _id>")
    desc = request.form.get("desc", "<missing desc")
    print("updating id=",_id)
    print("updating desc=",desc)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    _id = ObjectId(_id)
    shopping_list.update_one({'_id':_id}, {"$set" : {"desc": desc}})
    return redirect(url_for('get_list'))

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)