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
