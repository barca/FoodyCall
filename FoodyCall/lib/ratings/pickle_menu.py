from flask import Blueprint
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
import csv
import pickle

def pickle_menu():
    to_pickle = []
    try: 
        pickle_file = open('menu.pkl','rb')

    except:
        pickle_file = open('menu.pkl', 'wb')

    pickle_file.close()

    # Create Blueprint
    menu = Blueprint('menu', __name__, template_folder='templates')

    # Initialize connection with mongo :^)
    # This connects to the default port and host, localhost and 27017
    client = MongoClient()

    # Get the database
    db = client.menudb

    # Get the collection of items
    menu_items = db.menu_items

    for row in menu_items.find():
        sub_row = []
        for item in row:
           sub_row.append(item)
        to_pickle.append(row)

    pickle_file = open('menu.pkl', 'wb')
    pickle_dump = pickle.dump(to_pickle, pickle_file)
    pickle_file.close()

pickle_menu()