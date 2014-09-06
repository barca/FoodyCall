from flask import Blueprint
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
import csv
import sys
from datetime import datetime

client = MongoClient()
db = client.menudb
menu_items = db.menu_items

summies_menu_csv = csv.DictReader(open("menus.csv"))
for row in summies_menu_csv:
	row["rating_avg"] = int(row["rating_avg"])
	row["rater_count"] = int(row["rater_count"])
	row["price"] = float(row["price"])
	row["side"] = bool(int(row["side"]))
	row["menu"] = str(row["menu"])
	if row["filter"] == "none":
		row["filter"] = []
	else:
		row["filter"] = row["filter"].split(":")
	menu_items_id = menu_items.insert(row)