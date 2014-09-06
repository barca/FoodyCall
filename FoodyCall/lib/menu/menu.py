from flask import Blueprint
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
import csv


# Create Blueprint
menu = Blueprint('menu', __name__, template_folder='templates')


# Initialize connection with mongo :^)
# This connects to the default port and host, localhost and 27017
client = MongoClient()

# Get the database
db = client.menudb

# Get the collection of items
menu_items = db.menu_items

summies_menu = csv.DictReader(open("summies.csv"))
for row in summies_menu:
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
	print row

@menu.route('', methods = ['GET'])
def index():
	if request.method == "GET":
	 	ret = []
		for item in menu_items.find():
	 		item['_id'] = str(item['_id'])
	 		ret.append(item)

	 	return json.dumps(ret)
