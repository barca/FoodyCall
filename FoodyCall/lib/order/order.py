from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
import sender
from datetime import datetime, time

client = MongoClient()
db = client.menudb
menu_items = db.menu_items
order_history = db.order_history
order = Blueprint('order', __name__, template_folder = 'templates')
@order.route('',methods = ['POST'])
def index():
  dest = request.form.get('destination')
  if(dest == 's'):
      destination_num = 8607599700
  else:
    destination_num = 8607242526
  msg = "failed request"
  phone_num = request.form.get('number')
  food_id = request.form.get('item_id')
  try:
     side_id = request.form.get('side_id')
  except:
     pass
  special_requests = request.form.get('special')
  for items in menu_items.find():
    if food_id == str(items['_id']):
      msg = items['item']
  for items in menu_items.find():
    if side_id == str(items['_id']):
      side = items['item']
      msg = msg + " and " + side
  if(len(msg)<=0):
    return jsonify({'ERROR':"ID not found"})

  to_send = msg + ". " +special_requests
  rtn = sender.send_text(destination_num,"(978) 378-3121",to_send) #phone number should be here
  order= {
      'user' : phone_num,
      'side_id' : side_id,
      'item_id' : food_id,
      'date' : datetime.now(),
      'replied' : False
      }
  order_history.insert(order)
  if (rtn != 'success'):
    return jsonify({'ok':False})
  else:
    return jsonify({'ok':True})
