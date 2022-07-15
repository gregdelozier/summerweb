from mongita import MongitaClientDisk
client = MongitaClientDisk(host="./.mongita")

#----
shopping_db = client.shopping_db
shopping_list = shopping_db.shopping_list
shopping_list.delete_many({})

shopping_list.insert_one({"desc":"apple"})
shopping_list.insert_one({"desc":"milk"})
shopping_list.insert_one({"desc":"cheese"})
shopping_list.insert_one({"desc":"cookies"})
shopping_list.insert_one({"desc":"hot dogs"})
shopping_list.insert_one({"desc":"mustard"})

items = list(shopping_list.find({}))
items = [item['desc'] for item in items]
print(items)
