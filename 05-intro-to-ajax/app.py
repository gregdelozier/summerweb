from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")

app = Flask(__name__)

@app.route("/")
def get_list():
#   shopping_db = db_server.shopping_db
#   shopping_list = shopping_db.shopping_list

#    the_list = list(shopping_list.find({}))

#    print(the_list)

    return render_template('list.html')

@app.route("/add_item", methods=['GET'])
def get_add_item():
    return render_template('add_item.html')

@app.route("/data")
def get_data():
    data = { "data":[
    {
        "_id": "asdafga",
        "desc": "apples",
    },
    {
        "_id": "sdfsdf",
        "desc": "oranges",
    },
    ]}
    return data

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
