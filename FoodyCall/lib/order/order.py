from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
import sender

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
  msg = ""
  phone_num = request.form.get('number')
  food_id = request.form.get('item_id')
  try:
     side_id = request.form.get('side_id')
  except:
     pass
  special_requests = request.form.get('special')
  for items in menu_items.find():
    if food_id == str(items['id']):
      msg = items['item']
  for dog in menu_items.find():
    if side_id == str(items['id']):
      side = items['item']
      msg = side + msg
  if(len(msg)<=0):
    return jsonify({'ERROR':"ID not found"})
  to_send = msg + special_requests
  rtn = sender.send_text(phone_num,,to_send)
  order_time = time.time()
  order= {
      user : number,
      message : to_send,
      side_id : side_id,
      item_id : item_id,
      order_time : order_time
      }
  order_history.insert(order)
  if (rtn != 'success'):
    return jsonify({'ok':'false'})
  else:
    return jsonify({'ok':'true'})
