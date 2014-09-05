from flask import Flask
from lib.menu.menu import menu
from lib.utils.utils import utils
from pymongo import MongoClient
import csv

app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(utils, url_prefix='/utils')

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


@app.route('/')
def login():
    return "Enter your cell # here!"

if __name__ == '__main__':
    app.run()