from flask import Blueprint
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
	menu_items_id = menu_items.insert(row)

@menu.route('')
def index():
    return "Food goes here"