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
menu_items = db.menu_items

menu_to_serve = "none"

# Get the time and choose which menu to load, then get the collection of items
now = datetime.now()
if (now.hour >= 22 and now.hour <= 23) or now.hour == 0:
	menu_to_serve = "latenight"
elif (now.hour >= 11 and now.hour <= 2):
	menu_to_serve = "summies"
else:
	print "Invalid time: defaulting to summies for dev purposes"
	menu_to_serve = "summies"

@menu.route('', methods = ['GET'])
def index():
 	ret = []
	for item in menu_items.find():
		if menu_to_serve == "summies":
			if item["menu"] == "s":
				item['_id'] = str(item['_id'])
 				ret.append(item)
		elif menu_to_serve == "latenight":
			if item["menu"] == "ln":
				item['_id'] = str(item['_id'])
 				ret.append(item)
		else:
			print "Error"
			sys.exit(1)

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
		return jsonify(dct)