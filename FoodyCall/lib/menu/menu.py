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
		menulist = []
		for item in menu_items.find():
			menulist.append({"_id": str(item['_id']), 
				"description": item['description'], 
				"filter": item['filter'], "item": item['item'], 
				"menu": item['menu'], "price": item['price'], "rater_count": item['rater_count'], 
				"rating_avg": item['rating_avg'], "side": item['side'], "count": 0})

			for order in order_history.find():
				if str(number) == str(order['user']):
					if order['item_id'] == item['item_id']:
						item['count'] = item['count'] + 1
		return json.dumps(menulist)


