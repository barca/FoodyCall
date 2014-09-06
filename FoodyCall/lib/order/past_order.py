from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.menudb
menu_items = db.menu_items
order_history = db.order_history
past_order = Blueprint('past_order',__name__, template_folder = 'templates')

@past_order.route('')
def index():
  temp_item = {order_time : 0.00}
  phone_num = request.form.get('number')
  usr_history = []
  for item in order_history.find():
    if phone_num == str(item[user]):
      usr_history.append(item)
  for item in usr_history:
    if (float(item[order_time]) > temp[order_time]):
      temp_item = item;
  if item:
    return jsonify(item)
  else:
    return jsonify({'ERROR':'no prior order history'})

