from flask import Blueprint
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
import csv
import sys
from datetime import datetime


# Create Blueprint
menu = Blueprint('menu', __name__, template_folder='templates')

# Initialize connection with mongo :^)
# This connects to the default port and host, localhost and 27017.
client = MongoClient()

db = client.menudb
menu_to_serve = ""
menu_items = None

# Get the time and choose which menu to load, then get the collection of items
now = datetime.now()
if (now.hour >= 22 and now.hour <= 23) or now.hour == 0:
	menu_to_serve = "latenight"
	menu_items = db.latenight_menu
elif (now.hour >= 11 and now.hour <= 2):
	menu_to_serve = "summies"
	menu_items = db.summies_menu
else:
	print "Invalid time: defaulting to summies_menudb for dev purposes"
	menu_to_serve = "summies"
	menu_items = db.summies_menu

if menu_to_serve == "summies":
	summies_menu_csv = csv.DictReader(open("summies.csv"))
	for row in summies_menu_csv:
		row["rating_avg"] = int(row["rating_avg"])
		row["rater_count"] = int(row["rater_count"])
		row["price"] = float(row["price"])
		row["side"] = bool(int(row["side"]))
		row["extra"] = int(row["extra"])
		if row["filter"] == "none":
			row["filter"] = []
		else:
			row["filter"] = row["filter"].split(":")

		menu_items_id = menu_items.insert(row)

@menu.route('', methods = ['GET'])
def index():
 	ret = []
	for item in menu_items.find():
 		item['_id'] = str(item['_id'])
 		ret.append(item)

 	return json.dumps(ret)

order_history = db.order_history

@menu.route('/<number>')
def popular(number=9999999999):
		#number = request.form.get('number')
		dct = {}
		for order in order_history.find():
			if str(number) == str(order['user']):
				if order['item_id'] in dct:
					dct[order['item_id']] = dct[order['item_id']] + 1
				else:
					dct[order['item_id']] = 1
				if order['side_id'] in dct:
					dct[order['side_id']] = dct[order['side_id']] + 1
				else:
          dct[order['side_id']] = 1
    if(len(dict) < 1):
      return jsonify({"ERROR":"No User History"})
    return jsonify(dct)
